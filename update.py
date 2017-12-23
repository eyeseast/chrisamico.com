#!/usr/bin/env python

from links.load import LinkLoader
from tarbell_config import DATABASE_URL, LINK_TABLE, FEEDS

if __name__ == '__main__':
    LinkLoader(DATABASE_URL, LINK_TABLE, FEEDS)