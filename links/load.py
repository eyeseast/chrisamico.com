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
        "latitude": types.Float,
        "longitude": types.Float,
    }

    DB_OPTS = {"engine_kwargs": {"pool_recycle": 3600}}

    def __init__(self, database_url, table_name, feeds):

        self.database_url = database_url
        self.table_name = table_name

        # ensure a table
        db = dataset.connect(database_url)
        db[table_name]

        self.feeds = feeds
        self.queue = curio.Queue()

    def run(self, **kwargs):
        "Run with curio"
        curio.run(self.main(), **kwargs)

    async def main(self):
        "Do the whole download"

        prod_task = await curio.spawn(self.producer())
        cons_task = await curio.spawn(self.consumer())

        await prod_task.join()
        await cons_task.cancel()

    async def producer(self):
        async with curio.TaskGroup() as f:
            for name, url in self.feeds:
                try:
                    await f.spawn(self.handle_feed(name, url))
                except curio.TaskError as e:
                    print(e)

        await self.queue.join()

    async def consumer(self):
        while True:
            link = await self.queue.get()
            try:
                async with curio.timeout_after(10):
                    await curio.run_in_thread(self.save, link)

            except curio.TaskTimeout as e:
                print("Timed out: {feed}, {url}".format(**link))

            await self.queue.task_done()

    # run this in a thread
    def save(self, link):
        with dataset.connect(self.database_url, **self.DB_OPTS) as t:
            table = t[self.table_name]
            table.upsert(link, ["url"], types=self.TYPES)
            print("{feed}: {url}".format(**link))

    async def handle_feed(self, name, url):
        "Parse feed URL, enqueue links reading for the database"
        r = await curio.run_in_thread(requests.get, url)

        print(f"Loading {name}")
        feed = feedparser.parse(r.content)

        for entry in feed.entries:
            # bail here if we already have this URL
            # if self.table.find_one(_url=entry.link):
            #    continue

            date = get_entry_date(entry)

            try:
                og = await self.handle_link(
                    entry.link,
                    title=entry.get("title"),
                    # description=entry.get('description'),
                    url=entry.link,
                    date=date,
                    feed=name,
                )

                if og:
                    await self.queue.put(og)

            except Exception as e:
                print(e)

    async def handle_link(self, link, **defaults):
        "Fetch OG data and return a dict ready for the db"
        r = await curio.run_in_thread(requests.get, link)
        if r.ok:
            og = OpenGraph(html=r.content)
            defaults.update(og)
            defaults["_url"] = link

            return defaults


def get_entry_date(entry):
    "Get one of many possible date fields on a feed entry"
    date_fields = ["published_parsed", "updated_parsed", "created_parsed"]
    for field in date_fields:
        if field in entry and entry[field]:
            return datetime.datetime.fromtimestamp(time.mktime(entry[field]))

    else:
        print("No date for entry. Using now().\n{link}".format(**entry))
        return datetime.datetime.now()
