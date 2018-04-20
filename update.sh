#!/usr/bin/env sh

pipenv run ./app.py update
pipenv run datafreeze Freezefile.yaml

pipenv run ./app.py freeze

git commit -am "Updated: `date +%Y-%m-%d`"
git push origin master