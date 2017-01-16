# -*- coding: utf-8 -*-
"""
site settings
"""
import os
import sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)

import dataset
from flask import Blueprint, g

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
LINK_TABLE = "links"

FEEDS = (
    ('instapaper', 'https://www.instapaper.com/starred/rss/13475/qUh7yaOUGOSQeANThMyxXdYnho'),
    ('newsblur', 'https://chrisamico.newsblur.com/social/rss/35501/chrisamico'),
)

OG = {
    'title': 'This is my website',
    'type': 'website',
}

blueprint = Blueprint('blog', __name__)


def get_db():
    "Connect to DB"
    db = g.get('db', None)
    if db is None:
        db = dataset.connect(DATABASE_URL)
    return db


@blueprint.app_context_processor
def add_to_context():
    "Default context"
    db = get_db()
    links = db[LINK_TABLE]

    context = {
        'og': OG,
        'links': links,
    }

    return context