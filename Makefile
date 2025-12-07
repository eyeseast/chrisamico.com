# update everything

BLOG_DB=./db/blog.db
BLOG_BACKUP=./db/blog.sql
LINKS_CSV=./static/links.csv
LINKS_TABLE=links
FEEDS = \
 https://chrisamico.newsblur.com/social/rss/35501/chrisamico \
 https://www.instapaper.com/starred/rss/13475/qUh7yaOUGOSQeANThMyxXdYnho

install:
	uv sync

rebuild:
	sqlite3 $(BLOG_DB) < $(BLOG_BACKUP) 
	uv run sqlite-utils enable-wal $(BLOG_DB)

update:
	uv run ./links/update.py $(FEEDS)

freeze:
	uv run ./app.py freeze
	uv run sqlite-utils rows $(BLOG_DB) $(LINKS_TABLE) --csv > $(LINKS_CSV)

post:
	uv run ./links/mastodon.py

dump:
	sqlite3 $(BLOG_DB) .dump > $(BLOG_BACKUP)

run:
	uv run datasette serve --metadata metadata.yml db/*.db

shell:
	uv run ipython

preview:
	uv run ./app.py

.Phony: install rebuild update freeze run
