#!/usr/bin/env python
"""
Useful things
"""
import datetime
import time

import curio
import dataset
import feedparser
import requests

from sqlalchemy import types
from .opengraph import OpenGraph


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
        self.local = curio.Local()

        self.database_url = database_url
        self.table_name = table_name

        # ensure a table
        db = dataset.connect(database_url)
        db[table_name]

        self.feeds = feeds
        self.queue = curio.Queue()

    @property
    def table(self):
        return self.local.db[self.table_name]

    def run(self):
        "Run with curio"
        curio.run(self.main())

    async def main(self):
        "Do the whole download"

        # do the connection here
        # self.local.db = dataset.connect()

        prod_task = await curio.spawn(self.producer())
        cons_task = await curio.spawn(self.consumer())

        await prod_task.join()
        await cons_task.cancel()

    async def producer(self):
        async with curio.TaskGroup() as f:
            for name, url in self.feeds:
                await f.spawn(self.handle_feed(name, url))

        await self.queue.join()

    async def consumer(self):
        while True:
            link = await self.queue.get()
            await curio.run_in_thread(self.save, link)
            print('Saved link: {url}'.format(**link))

            await self.queue.task_done()

    # run this in a thread
    def save(self, link):
        with dataset.connect(self.database_url) as t:
            table = t[self.table_name]
            table.upsert(link, ['url'], types=self.TYPES)

    async def handle_feed(self, name, url):
        "Parse feed URL, enqueue links reading for the database"
        r = await curio.run_in_thread(requests.get, url)
        feed = feedparser.parse(r.content)

        for entry in feed.entries:
            # bail here if we already have this URL
            #if self.table.find_one(_url=entry.link):
            #    continue

            date = get_entry_date(entry)

            og = await self.handle_link(entry.link, 
                title=entry.get('title'),
                #description=entry.get('description'),
                url=entry.link,
                date=date,
                feed=name)

            if og:
                await self.queue.put(og)

    async def handle_link(self, link, **defaults):
        "Fetch OG data and return a dict ready for the db"
        r = await curio.run_in_thread(requests.get, link)
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

