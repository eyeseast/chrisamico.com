# update everything

BLOG_DB=./db/blog.db
LINKS_CSV=./static/links.csv
LINKS_TABLE=links
FEEDS = \
 https://chrisamico.newsblur.com/social/rss/35501/chrisamico \
 https://www.instapaper.com/starred/rss/13475/qUh7yaOUGOSQeANThMyxXdYnho

rebuild:
	pipenv run sqlite-utils upsert --csv --alter --pk id $(BLOG_DB) $(LINKS_TABLE) $(LINKS_CSV)

update:
	#pipenv run feed-to-sqlite --table $(LINKS_TABLE) $(BLOG_DB) $(FEEDS)
	pipenv run ./links/update.py $(FEEDS)

run:
	pipenv run datasette serve --metadata metadata.yml db/*.db
