---
title: My Python setup, as of January 2023
summary: The Python landscape can be a confusing mess of overlapping tools that sometimes don't work well together. This is my setup.
---

This is my recommended Python setup, as of January 2023. The Python landscape can be a [confusing mess of overlapping tools](https://xkcd.com/1987/) that sometimes don't work well together. I wrote this for my team at work, which included (at the time) a designer and several developers used to working in Node.js and Go. This was an effort to standardize our environments.

## Tools and helpful links:

- Python docs: <https://docs.python.org/3/>
- Python Standard Library: <https://docs.python.org/3/library/index.html> - Start here when you're trying to solve a specific problem
- pip: <https://pip.pypa.io/en/stable/> - Python's standard package installer, included with the language itself
- pipx: <https://pipxproject.github.io/pipx/> - Global script installer, built on top of pip
- pipenv: <https://pipenv.pypa.io/en/latest/> - Package installer for projects, manages both dependencies and virtual environments
- pyenv: <https://github.com/pyenv/pyenv> - Manage different versions of Python itself
- homebrew: <https://brew.sh/> - Package manager for macOs, use for specific needs
- Postgres.app: <https://postgresapp.com/> - Preferred database server for macOs

## Installing the right Python

Python 3 is now the right version of Python to use. We may have projects running different minor versions – such as 3.7 or 3.9 – but we should always default to the latest available version. As of this writing, that's 3.11.1. The must up-to-date Python documentation will always be here: https://docs.python.org/3/.

In the past, you might have seen recommendations to install Python with homebrew. This is now strongly discouraged. Let me say that louder: **DO NOT INSTALL PYTHON WITH HOMEBREW**. Homebrew can be very aggressive and expansive with upgrades, and upgrading one package often results in lots of seemingly unrelated upgrades, which will frequently break dependencies for other packages.

**Use pyenv**. To install and manage different Python versions, use pyenv. In most cases, I recommend either the homebrew installation or the git installation:

```sh
brew update
brew install pyenv
```

Is it weird that I recommend using homebrew to install pyenv but not Python? Yes it is. But pyenv is built entirely with shell scripts, so it's relatively safe, and pyenv itself will keep your Python versions safely isolated from homebrew's aggressive upgrades.

Follow the instructions to configure your shell profile (https://github.com/pyenv/pyenv#installation) so that the pyenv command is available and you are able to install new versions of Python as needed.

From there, install at least the latest stable version of Python (again, probably 3.11.1) and make that your global default. This will make the right version of pip available for installing new packages.

```sh
pyenv install --list # see a list of installable versions
pyenv install 3.11.1 # or something different
pyenv global 3.11.1

python --version
# Python 3.11.1

which python
# /Users/camico/.pyenv/shims/python

which pip
# /Users/camico/.pyenv/shims/pip
```

## Global scripts and utilities

For any tools built in Python you want available across projects, use `pipx`. Install it with `pip`:

```sh
pip install --user pipx # install it
pipx ensurepath # make sure your system can find it
```

_(Note that pipx's documentation recommends installing with Homebrew. As noted above, I don't recommend using Homebrew with Python projects, except for pyenv.)_

Among the first things you should install with `pipx` is `pipenv`, which we'll use for specific projects.

## Virtual environments

Python uses virtual environments to separate dependencies for different projects. This can be a frustrating step, especially if you are used to having a local `node_modules` folder. In the past, this also meant having to install a separate `virtualenv` library. In Python 3, it's now part of the standard library as the `venv` package.

This is a good tutorial that covers how virtual environments work: https://docs.python.org/3/tutorial/venv.html

Here's the tl;dr:

```sh
python -m venv project-dir

source project-dir/bin/activate
```

That will create a virtual environment in the `project-dir` folder. The second command will run the activate script, which will tell your shell to use a local version of Python and locally installed dependencies. For the most part, you won't have to do this by hand, but it's useful to know what's happening under the hood.

In a project with a `Pipfile`, like [alltheplaces-datasette](https://github.com/eyeseast/alltheplaces-datasette), we can use `pipenv` to both manage our virtual environment and install dependencies. In that case, navigate to the directory and run `pipenv sync`:

```sh
cd alltheplaces-datasette
pipenv sync
```

This will also, assuming you have pyenv installed and working, switch to the version of Python listed in the `Pipfile` (installing it if needed). Consult the [pipenv docs](https://pipenv.pypa.io/en/latest/) to see what else it can do.

In practice, I almost never use a virtual environment by itself. My standalone projects, like [alltheplaces-datasette](https://github.com/eyeseast/alltheplaces-datasette), will always include a `Pipfile` and `Pipfile.lock`. When I work on open source libraries (mine or not), I still use `pipenv`. Running `pipenv install -e .` will create a virtual environment with that library and its dependencies.

If I need to run Python commands inside a virtual environment, I use `pipenv shell` or `pipenv run`.

## Installing local Python packages

For the most part, we're going to work on projects where we have a `Pipfile` managing dependencies. In that case, installing something new is a one-liner:

```sh
pipenv install django
```

That will install the `django` package, add it to our `Pipfile` and update our `Pipfile.lock` file, pinning a specific version. Running `pipenv sync`, as above, installs dependencies from `Pipfile.lock`, much like `npm ci` installs from `package-lock.json`, ensuring we get the same version of every dependency every time.

## Databases

There are two main databases I use with Python: [SQLite](https://sqlite.org/) and [Postgres](https://www.postgresql.org/).

SQLite comes bundled with Python, though I use a more recent version installed via Homebrew. (That's worth a post in itself.) It runs as an embedded process, with all data contained in a single file, and it can be very useful for data analysis.

Postgres is the best database available for web applications. For local development, I recommend `Postgres.app`, which the easiest way to manage a database server on your laptop.

_So that's it. It's a lot. Why is Python so complicated to set up right? I'll get into that in a future post._
