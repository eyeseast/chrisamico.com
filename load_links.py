#!/usr/bin/env python
"""
Useful things
"""
import datetime
import time

import dataset
import feedparser
import requests

from opengraph import OpenGraph
from sqlalchemy import types
from tarbell_config import FEEDS, DATABASE_URL, LINK_TABLE


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
                if self.table.upsert(link, ['url'], types=self.TYPES):
                    print(link['url'])

    def handle_feed(self, name, url):
        "Parse feed URL, yield links reading for the database"
        r = requests.get(url)
        feed = feedparser.parse(r.content)

        for entry in feed.entries:
            # bail here if we already have this URL
            #if self.table.find_one(_url=entry.link):
            #    continue

            if 'published_parsed' in entry:
                date = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
            else:
                date = datetime.datetime.now()

            og = self.handle_link(entry.link, 
                title=entry.get('title'),
                description=entry.get('description'),
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


def main():
    """
    Run a LinkLoader
    """
    LinkLoader(DATABASE_URL, LINK_TABLE, FEEDS).run()


if __name__ == '__main__':
    main()