#!/usr/bin/env python

import os
import sys

import dataset
from flask import Flask, g, render_template
from flask_frozen import Freezer
from markdown import markdown as md

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
LINK_TABLE = "links"

OG = {
    'title': 'This is my website',
    'type': 'website',
}

app = Flask(__name__)

def get_db():
    "Connect to DB"
    db = g.get('_database', None)
    if db is None:
        db = dataset.connect(DATABASE_URL)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.engine.dispose()


@app.template_filter('markdown')
def markdown(s):
    return md(s)


@app.context_processor
def add_to_context():
    "Default context"
    db = get_db()
    links = db[LINK_TABLE]

    context = {
        'og': OG,
        'links': links.find(order_by='-date'),
    }

    return context


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)