#!/usr/bin/env python

import os
import sys
from urllib import parse

import dataset

# from dotenv import load_dotenv, find_dotenv
from flask import Flask, g, render_template, send_from_directory
from flask_frozen import Freezer
from markdown import markdown as md

from links.load import LinkLoader

# load_dotenv(find_dotenv())


DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/chrisamico.com")
LINK_TABLE = "links"

FEEDS = (
    (
        "instapaper",
        "https://www.instapaper.com/starred/rss/13475/qUh7yaOUGOSQeANThMyxXdYnho",
    ),
    ("newsblur", "https://chrisamico.newsblur.com/social/rss/35501/chrisamico"),
)

FREEZER_RELATIVE_URLS = True
FREEZER_DESTINATION = "docs"
FREEZER_DESTINATION_IGNORE = ["CNAME"]

TEMPLATES_AUTO_RELOAD = True

OG = {"title": "Chris Amico, journalist & programmer", "type": "website"}

CONTACT = {
    "twitter": "https://twitter.com/eyeseast",
    "github": "https://github.com/eyeseast",
    "linkedin": "https://www.linkedin.com/in/chrisamico/",
    "name": "Chris Amico",
    "tagline": "Journalist & programmer",
}

app = Flask(__name__)
app.config.from_object(__name__)

freezer = Freezer(app)


def get_db():
    "Connect to DB"
    db = g.get("_database", None)
    if db is None:
        db = g._database = dataset.connect(DATABASE_URL)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.engine.dispose()


@app.template_filter("date")
def date(d, format="%b %d, %Y"):
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

    context = {"OG": OG, "CONTACT": CONTACT}

    return context


@app.route("/")
def index():
    db = get_db()
    links = db[LINK_TABLE]

    links = links.find(order_by="-date", _limit=20)

    return render_template("index.html", links=links)


@app.route("/<name>.txt")
def textfile(name):
    "Send a text file"
    filename = f"{name}.txt"
    return send_from_directory("./txt", filename)


@freezer.register_generator
def txt_urls():
    for filename in os.listdir("./txt"):
        yield "textfile", {"name": os.path.splitext(filename)[0]}


if __name__ == "__main__":
    if sys.argv[1:]:
        if sys.argv[1] == "update":
            LinkLoader(DATABASE_URL, LINK_TABLE, FEEDS).run(with_monitor=True)

        elif sys.argv[1] == "freeze":
            freezer.freeze()

    else:
        app.run(debug=True)
