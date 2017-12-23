#!/usr/bin/env python
"""
Useful things
"""
import datetime
import time

import dataset
import feedparser
import requests

from .opengraph import OpenGraph
from sqlalchemy import types


class LinkLoader(object):
    """
    Loop through FEEDS
    Fetch open graph data for each link
    Save OG for each (plus some other metadata) to database
    """
    TYPES = {
        'latitude': types.Float,
        'longitude': types.Float,
    }

    def __init__(self, database_url, table_name, feeds):
        self.db = dataset.connect(database_url)
        self.table = self.db[table_name]
        self.feeds = feeds

    def run(self):
        "Do the whole download"
        for name, url in self.feeds:
            for link in self.handle_feed(name, url):
                self.table.upsert(link, ['url'], types=self.TYPES)

    def handle_feed(self, name, url):
        "Parse feed URL, yield links reading for the database"
        r = requests.get(url)
        feed = feedparser.parse(r.content)

        for entry in feed.entries:
            # bail here if we already have this URL
            #if self.table.find_one(_url=entry.link):
            #    continue

            date = get_entry_date(entry)

            og = self.handle_link(entry.link, 
                title=entry.get('title'),
                #description=entry.get('description'),
                url=entry.link,
                date=date,
                feed=name)

            if og:
                yield og

    def handle_link(self, link, **defaults):
        "Fetch OG data and return a dict ready for the db"
        r = requests.get(link)
        if r.ok:
            og = OpenGraph(html=r.content)
            defaults.update(og)
            defaults['_url'] = link

            return defaults


def get_entry_date(entry):
    "Get one of many possible date fields on a feed entry"
    date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']
    for field in date_fields:
        if field in entry and entry[field]:
            return datetime.datetime.fromtimestamp(time.mktime(entry[field]))

    else:
        print('No date for entry. Using now().\n{link}'.format(**entry))
        return datetime.datetime.now()

