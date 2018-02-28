#!/usr/bin/env sh

python app.py update
datafreeze Freezefile.yaml

python app.py freeze

git commit -am "Updated: `date +%Y-%m-%d`"
git push origin master