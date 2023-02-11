# update everything

BLOG_DB=./db/blog.db
LINKS_CSV=./static/links.csv
LINKS_TABLE=links
FEEDS = \
 https://chrisamico.newsblur.com/social/rss/35501/chrisamico \
 https://www.instapaper.com/starred/rss/13475/qUh7yaOUGOSQeANThMyxXdYnho

install:
	pipenv sync

rebuild:
	# pipenv run sqlite-utils upsert --csv --alter --pk id $(BLOG_DB) $(LINKS_TABLE) $(LINKS_CSV)

update:
	pipenv run ./links/update.py $(FEEDS)

freeze:
	pipenv run ./app.py freeze
	pipenv run sqlite-utils rows $(BLOG_DB) $(LINKS_TABLE) --csv > $(LINKS_CSV)

run:
	pipenv run datasette serve --metadata metadata.yml db/*.db

shell:
	pipenv run ipython

.Phony: install rebuild update freeze run
