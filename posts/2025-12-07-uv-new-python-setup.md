---
title: My Python setup, December 2025
summary: uv is in, everything else is out.
---

I'm at the point where I'm migrating all my projects to [uv](https://docs.astral.sh/uv/), and new Python projects don't use any other package manager.

I finally got around to migrating _this site_ to use it, using the very handy [migrate-to-uv](https://github.com/mkniewallner/migrate-to-uv) tool. So it's time to update my recommended Python setup.

My [old Python setup](https://chrisamico.com/blog/2023-01-14/python-setup/) was very much built around the complications of managing environments and dependencies, and the conflicting set of tools to deal with those two problems. There are still a few places where I'll use [pipx](https://pipx.pypa.io/stable/), but otherwise everything is on `uv`.

This guide is still aimed at a recent Apple or Linux computer, or [WSL](https://learn.microsoft.com/en-us/windows/wsl/) if you're on Windows. I'm writing this on a MacBook Pro with an M2 chip, if that matters to you.

## Tools and helpful links:

- Python docs: <https://docs.python.org/3/>
- Python Standard Library: <https://docs.python.org/3/library/index.html> - Start here when you're trying to solve a specific problem
- uv: <https://docs.astral.sh/uv/> - For packaging, dependency and environment management, plus standalone scripts
- pipx: <https://pipxproject.github.io/pipx/> - Global script installer, built on top of pip
- homebrew: <https://brew.sh/> - Package manager for macOs, use for specific needs
- Postgres.app: <https://postgresapp.com/> - Preferred database server for macOs

You probably don't need both `uv` and `pipx`. I have a bunch of existing tools I installed with `pipx`, and those work fine, so I haven't migrated them to `uvx`.

There is one set of tools that stays on `pipx`, though: Datasette and its SQLite toolchain. Simon Willison built those to install their own plugins, using `datasette install <plugin>` or `llm install <plugin>`. Those use `pip` internally and sometimes `uv` can cause problems upgrading, so I've kept them on `pipx`.

## Installing the right Python

Use `uv` and nothing else for this. Run `uv python list` to see what's already installed or otherwise available. If you're not using `pipx`, it's fine to just let `uv` install the right version of Python for each project.

If you want a specific version of Python installed globally, use `uv python install <version>`. The [docs](https://docs.astral.sh/uv/guides/install-python/) are good.

For `pipx`, stick to my instructions from a couple years ago:

```sh
pip install --user pipx # install it
pipx ensurepath # make sure your system can find it
```

That's assuming your system already comes with a vesion of Python and `pip` installed. If not, try [Homebrew](https://pipx.pypa.io/stable/installation/). Maybe it's better now, especially with `uv` managing everything else.

## Virtual environments and local dependencies

Everything is now part of `uv`. Run `uv init` to create a project, `uv add` for each dependency and `uv sync` to install everything from an existing project.

Use `uv run` to run scripts inside the virtual environment that `uv` creates.

## This is easier now

I never managed to write the post about why Python's setup is so hard. It ultimately comes down to dependencies, both libraries and Python itself. For the most part, `uv` has made this a non-issue. It's also significantly faster than the tools it replaced, which means I can iterate faster and don't lose focus waiting for dependencies to download and install.

Now, to migrate more projects ...
