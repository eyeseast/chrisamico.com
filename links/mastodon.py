#!/usr/bin/env python
"""
Send recent links to Mastodon
"""
import datetime
import enum
import json
import logging
from pathlib import Path

from sqlite_utils.db import Database
from toot.config import load_app, load_user
from toot.api import post_status

from update import TABLE_NAME as LINKS_TABLE

USER = "chrisamico"
HOST = "journa.host"


log = logging.getLogger("links.mastodon")
log.setLevel(logging.DEBUG)

logging.basicConfig()


ROOT = Path(__file__).parent.parent.absolute()
DB_PATH = ROOT / "db" / "blog.db"
TABLE_NAME = "mastodon"

UpdateStatus = enum.StrEnum("status", ["success", "failed"])


def get_updated_table():
    db = Database(DB_PATH)
    table = db[TABLE_NAME]

    if not table.exists():
        table.create(
            {
                "link_id": str,
                "posted": datetime.datetime,
                "status": str,
                "post_url": str,
                "error": str,
            },
            foreign_keys=[("link_id", LINKS_TABLE, "id")],
        )

    return table


def post_latest(dry_run=False):
    "Post the latest un-posted link to Mastodon"
    db = Database(DB_PATH)
    sql = f"select * from {LINKS_TABLE} order by published desc limit 1"
    latest = next(db.query(sql), None)

    if not latest:
        return log.error("No links in %s table", LINKS_TABLE)

    log.info("Posting link: %s", latest["link"])

    if dry_run:
        print(link_text(latest))
        return

    post_link(latest)


def post_all(dry_run=False):
    "Post all un-posted links"
    db = Database(DB_PATH)
    sql = Path(__file__).parent / "links_to_post.sql"

    latest = db.query(sql.read_text())
    updates = get_updated_table()

    for link in latest:
        if dry_run:
            print(link_text(link))
        else:
            post_link(link)


def post_link(link):
    "post the update and record that I did it"
    updates = get_updated_table()
    app = load_app(HOST)
    user = load_user(f"{USER}@{HOST}")
    text = link_text(link)

    update = {"link_id": link["id"]}
    try:
        result = post_status(app, user, text)
        update.update(
            {
                "posted": result["created_at"],
                "status": UpdateStatus.success,
                "post_url": result["url"],
            }
        )
    except Exception as e:
        update.update({"status": UpdateStatus.failed, "error": str(e)})

    updates.insert(update)


def link_text(link):
    og = safe_json(link.get("og", "")) or {}
    if og.get("site_name"):
        return f"{link['title']} ({og['site_name']}): {link['link']}"
    return f"{link['title']}: {link['link']}"


def safe_json(s):
    try:
        return json.loads(s)
    except:
        return None


if __name__ == "__main__":
    post_all()
