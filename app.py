#!/usr/bin/env python3

import datetime
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib import parse
from zoneinfo import ZoneInfo

import frontmatter
import yaml

from dateutil.parser import parse as date_parse
from feedgen.feed import FeedGenerator
from flask import (
    Flask,
    Response,
    abort,
    g,
    render_template,
    send_from_directory,
    url_for,
)
from flask_frozen import Freezer
from markdown import Markdown
from sqlite_utils import Database

ROOT = Path(__file__).parent.absolute()
DB_PATH = ROOT / "db" / "blog.db"
LINK_TABLE = "links"

PORTFOLIO = ROOT / "db" / "portfolio.yml"

FREEZER_RELATIVE_URLS = True
FREEZER_DESTINATION = "dist"
FREEZER_DESTINATION_IGNORE = ["CNAME"]

TEMPLATES_AUTO_RELOAD = True
TIMEZONE = ZoneInfo("US/Eastern")

PORT = int(os.environ.get("PORT", 8000))

OG = {
    "title": "Chris Amico, journalist & programmer",
    "type": "website",
    "author": "Chris Amico",
    "url": "https://chrisamico.com",
    "description": "Journalist & programmer",
}

CONTACT = {
    "twitter": "https://twitter.com/eyeseast",
    "github": "https://github.com/eyeseast",
    "linkedin": "https://www.linkedin.com/in/chrisamico/",
    "name": "Chris Amico",
    "tagline": "Journalist & programmer",
}

POST_FILENAME_RE = re.compile(
    r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(?P<slug>.+)$"
)

LINKS_PER_PAGE = 20

md = Markdown(
    extensions=[
        "markdown.extensions.codehilite",
        "markdown.extensions.fenced_code",
        "markdown.extensions.smarty",
        "markdown.extensions.tables",
    ]
)

app = Flask(__name__)
app.config.from_object(__name__)

freezer = Freezer(app)


def get_db():
    "Connect to DB"
    db = g.get("_database", None)
    if db is None:
        db = g._database = Database(DB_PATH)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.template_filter("date")
def date(d, format="%b %d, %Y"):
    if not isinstance(d, (datetime.datetime, datetime.date)):
        d = date_parse(d)
    return d.strftime(format)


@app.template_filter("markdown")
def markdown(s):
    return md.convert(s)


@app.template_filter("urlparse")
def urlparse(url, part="netloc"):
    "Parse a URL and return part of it"
    u = parse.urlparse(url)
    return getattr(u, part, None)


@app.context_processor
def add_to_context():
    "Default context"

    context = {"OG": OG, "CONTACT": CONTACT, "timestamp": time.time()}

    return context


@app.route("/")
def index():
    db = get_db()
    links = db[LINK_TABLE]

    links = links.rows_where(order_by="published desc", limit=LINKS_PER_PAGE + 1)
    links = json_cols(links, ["og"])
    links = list(links)

    has_next = len(links) > LINKS_PER_PAGE

    return render_template(
        "index.html", links=links, page=1, has_next=has_next, has_previous=False
    )


@app.route("/links/")
@app.route("/links/<int:page>/")
def links(page=1):
    db = get_db()
    links = db[LINK_TABLE]

    if page > 1:
        offset = LINKS_PER_PAGE * (page - 1)
        links = links.rows_where(
            order_by="published desc", limit=LINKS_PER_PAGE + 1, offset=offset
        )
    else:
        links = links.rows_where(order_by="published desc", limit=LINKS_PER_PAGE + 1)

    links = json_cols(links, ["og"])
    links = list(links)

    has_next = len(links) > LINKS_PER_PAGE

    return render_template(
        "index.html",
        links=links,
        page=page,
        has_next=has_next,
        has_previous=page > 1,
    )


# blog
@app.route("/blog/")
def post_index():
    files = sorted(Path("posts").glob("*.md"), reverse=True)
    posts = map(frontmatter.load, files)
    posts = [process_post(post, filename) for post, filename in zip(posts, files)]

    return render_template("post_index.html", posts=posts)


@app.route("/blog/<date>/<slug>/")
def post_detail(date, slug):
    path = Path(f"posts/{date}-{slug}.md")
    if not path.exists():
        abort(404)

    post = frontmatter.load(path)
    post = process_post(post, path)

    post_og = dict(OG)
    post_og["title"] = post["title"]

    return render_template("post_detail.html", post=post, OG=post_og)


# feeds
@app.route("/blog.rss")
def blog_feed():
    files = sorted(Path("posts").glob("*.md"), reverse=True)[:10]
    posts = map(frontmatter.load, files)
    posts = [process_post(post, filename) for post, filename in zip(posts, files)]

    feed = FeedGenerator()
    feed.id(OG["url"])
    feed.title(OG["title"])
    feed.author(name=OG["author"])
    feed.link(href=OG["url"], rel="self")
    feed.description(OG["description"])

    for post in posts:
        entry = feed.add_entry(order="append")
        entry.title(post["title"])
        entry.id(post["url"])
        entry.link(href=OG["url"] + post["url"])
        entry.summary(post.get("summary") or post.content)
        entry.description(post.content)
        entry.published(post["date"])

    return Response(feed.rss_str(), content_type="application/rss+xml")


@app.route("/links.rss")
def links_feed():
    db = get_db()
    links = db[LINK_TABLE]

    links = links.rows_where(order_by="published desc", limit=20)
    links = json_cols(links, ["og"])

    feed = FeedGenerator()
    feed.id(OG["url"])
    feed.title(f'{OG["title"]}: Links')
    feed.author(name=OG["author"])
    feed.link(href=OG["url"], rel="self")
    feed.description(OG["description"])

    for link in links:
        entry = feed.add_entry(order="append")
        entry.title(link["title"])
        entry.link(href=link["link"])
        entry.description(link["description"])
        entry.published(link["published"])

    return Response(feed.rss_str(), content_type="application/rss+xml")


@app.route("/portfolio/")
def portfolio():
    data = yaml.load(PORTFOLIO.read_text(), Loader=yaml.Loader)
    return render_template("portfolio.html", **data)


@app.route("/<name>.txt")
def textfile(name):
    "Send a text file"
    filename = f"{name}.txt"
    return send_from_directory("./txt", filename)


@freezer.register_generator
def txt_urls():
    for filename in os.listdir("./txt"):
        yield "textfile", {"name": os.path.splitext(filename)[0]}


def json_cols(rows, columns):
    for row in rows:
        for column in columns:
            row[column] = json.loads(row[column])
        yield row


def process_post(post: frontmatter.Post, path: Path):
    m = POST_FILENAME_RE.match(path.stem)
    post.metadata.update(m.groupdict())
    post["date"] = datetime.datetime(
        int(post["year"]), int(post["month"]), int(post["day"]), tzinfo=TIMEZONE
    )

    post["path"] = path
    post["url"] = url_for(
        "post_detail", date=post["date"].strftime("%Y-%m-%d"), slug=post["slug"]
    )
    post.content = md.convert(post.content)

    return post


if __name__ == "__main__":
    if sys.argv[1:] and sys.argv[1] == "freeze":
        freezer.freeze()

    else:
        app.run(debug=True, port=PORT)
