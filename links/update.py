#!/usr/bin/env python3
"""
Update links table using feed-to-sqlite with a normalize function that fetches OpenGraph tags
"""
import logging
import sys
from pathlib import Path

import httpx
from dateutil.parser import parse
from feed_to_sqlite.ingest import ingest_feed, extract_entry_fields

from opengraph import OpenGraph

log = logging.getLogger("links.update")
log.setLevel(logging.DEBUG)

logging.basicConfig()

ROOT = Path(__file__).parent.parent.absolute()
DB_PATH = ROOT / "db" / "blog.db"
TABLE_NAME = "links"


def main(*urls):
    with httpx.Client(timeout=30) as client:
        for url in urls:
            log.info("Loading feed: %s", url)
            ingest_feed(
                DB_PATH,
                url=url,
                table_name=TABLE_NAME,
                normalize=normalize,
                client=client,
                alter=True,
            )


def normalize(table, entry, feed_details, client):
    log.info("%s: %s", feed_details.title, entry.title)
    row = extract_entry_fields(table, entry, feed_details)

    try:
        og = OpenGraph.fetch(entry["link"], client=client)
    except Exception as e:
        log.error(e)
        return row

    if og.get("url"):
        row["link"] = og.pop("url")

    # not sure why this needs to be done separately, but here we are
    if og.get("description"):
        row["description"] = og.pop("description")

    for key in row:
        if og.get(key):
            row[key] = og.pop(key)

    row["published"] = safe_date(row.get("published"))
    row["updated"] = safe_date(row.get("updated"))

    row["og"] = dict(og)

    return row


def safe_date(s, default=None):
    if not s:
        return default

    try:
        return parse(s)
    except:
        return default


if __name__ == "__main__":
    main(*sys.argv[1:])
