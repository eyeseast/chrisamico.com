# update everything

BLOG_DB=./db/blog.db
BLOG_BACKUP=./db/blog.sql
LINKS_CSV=./static/links.csv
LINKS_TABLE=links
FEEDS = \
 https://chrisamico.newsblur.com/social/rss/35501/chrisamico \
 https://www.instapaper.com/starred/rss/13475/qUh7yaOUGOSQeANThMyxXdYnho

install:
	pipenv sync

rebuild:
	sqlite3 $(BLOG_DB) < $(BLOG_BACKUP) 

update:
	pipenv run ./links/update.py $(FEEDS)

freeze:
	pipenv run ./app.py freeze
	pipenv run sqlite-utils rows $(BLOG_DB) $(LINKS_TABLE) --csv > $(LINKS_CSV)

post:
	pipenv run ./links/mastodon.py

dump:
	sqlite3 $(BLOG_DB) .dump > $(BLOG_BACKUP)

run:
	pipenv run datasette serve --metadata metadata.yml db/*.db

shell:
	pipenv run ipython

preview:
	pipenv run ./app.py

.Phony: install rebuild update freeze run
