#!/usr/bin/env python3

import datetime
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib import parse

import frontmatter
from dateutil.parser import parse as date_parse
from flask import Flask, abort, g, render_template, send_from_directory
from flask_frozen import Freezer
from markdown import markdown as md
from sqlite_utils import Database

ROOT = Path(__file__).parent.absolute()
DB_PATH = ROOT / "db" / "blog.db"
LINK_TABLE = "links"


FREEZER_RELATIVE_URLS = True
FREEZER_DESTINATION = "docs"
FREEZER_DESTINATION_IGNORE = ["CNAME"]

TEMPLATES_AUTO_RELOAD = True

OG = {
    "title": "Chris Amico, journalist & programmer",
    "type": "website",
    "author": "Chris Amico",
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
        # db.engine.dispose()
        pass


@app.template_filter("date")
def date(d, format="%b %d, %Y"):
    if not isinstance(d, (datetime.datetime, datetime.date)):
        d = date_parse(d)
    return d.strftime(format)


@app.template_filter("markdown")
def markdown(s):
    return md(s)


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

    links = links.rows_where(order_by="published desc", limit=20)
    links = json_cols(links, ["og"])

    return render_template("index.html", links=links)


@app.route("/blog/")
def post_index():
    files = list(Path("posts").glob("*.md"))
    posts = map(frontmatter.load, files)
    posts = [process_post(post, filename) for post, filename in zip(posts, files)]

    return render_template("post_index.html", posts=reversed(posts))


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
    post["date"] = datetime.date(
        int(post["year"]), int(post["month"]), int(post["day"])
    )

    post["path"] = path
    post["url"] = "/blog/{date}/{slug}/".format(
        date=post["date"].strftime("%Y-%m-%d"), slug=post["slug"]
    )
    post.content = md(post.content)

    return post


if __name__ == "__main__":
    if sys.argv[1:] and sys.argv[1] == "freeze":
        freezer.freeze()

    else:
        app.run(debug=True)
