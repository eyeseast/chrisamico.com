#!/usr/bin/env python3
"""
Update links table using feed-to-sqlite with a normalize function that fetches OpenGraph tags
"""
import logging
import sys
from pathlib import Path

import httpx
from feed_to_sqlite.ingest import ingest_feed, extract_entry_fields

from opengraph import OpenGraph

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

ROOT = Path(__file__).parent.parent.absolute()
DB_PATH = ROOT / "db" / "blog.db"
TABLE_NAME = "links"


def main(*urls):
    with httpx.Client(timeout=30) as client:
        for url in urls:
            ingest_feed(
                DB_PATH,
                url=url,
                table_name=TABLE_NAME,
                normalize=normalize,
                client=client,
                alter=True,
            )


def normalize(table, entry, feed_details, client):
    logging.info("%s: %s", feed_details.title, entry.title)
    og = OpenGraph.fetch(entry["link"], client=client)
    row = extract_entry_fields(table, entry, feed_details)

    if og.get("url"):
        row["link"] = og.pop("url")

    # not sure why this needs to be done separately, but here we are
    if og.get("description"):
        row["description"] = og.pop("description")

    for key in row:
        if og.get(key):
            row[key] = og.pop(key)

    row["og"] = dict(og)

    return row


if __name__ == "__main__":
    main(*sys.argv[1:])
