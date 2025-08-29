---
title: Migrating a small Python library to uv
summary: There should be one -- and preferably only one -- obvious way to do it.
---

A lot of my old Python projects are sitting in limbo these days, because I started them using an old packaging system that I've since abandoned. There was the `pip-tools` phase, the `pipenv` era, a brief interlude with `poetry`. Some just used `virtualenv` (or `virtualenvwrapper` or `python -m venv`).

I would like to move all of these onto `uv`, because I think it does everything these other tools do, and does all of it faster and in only one tool.

Python's biggest shortcoming has always been [setting up a development environment](https://chrisamico.com/blog/2023-01-14/python-setup/), but `uv` really does solve a lot of these problems.

I wanted to fix a bug on [feed-to-sqlite](https://github.com/eyeseast/feed-to-sqlite) yesterday, so I decided it migrate it to `uv` first. Here's what I did and where I ran into obstacles.

There is a tool called [`migrate-to-uv`](https://github.com/mkniewallner/migrate-to-uv) that seemed like it would do this for me in one step. It covers most package managers, but I wasn't actually using one of those. I used an old fashioned `setup.py` file and `setuptools`, because Python's packaging ecosystem has largely split into tools for libraries and tools for projects. So I had to do this by hand.

The newer standard, which seems to unify libraries and projects, is [pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/). (But [`setup.py` still works](https://packaging.python.org/en/latest/discussions/setup-py-deprecated/#setup-py-deprecated), sort of, if you're using `setuptools`.)

Running `uv init --lib` generated a stub `pyproject.toml` file. I tried a couple versions of `init`; using the `--lib` skipped making a `main.py` file that I'd have to delete and picked up some of the existing project metadata. From there, it was a lot of copy/paste from `setup.py` to `pyproject.toml`. Nothing hard, but it would be nice to automate this. Bits of metadata go in unexpected places, but it's fine and the documentation is good.

Since `pyproject.toml` is agnostic on how you build and publish, you have to tell it what packaging system you're using. This is what `uv` [needs](https://docs.astral.sh/uv/concepts/build-backend/#using-the-uv-build-backend) (as of yesterday, at least; check the docs whenever you do this because everything changes):

```toml
[build-system]
requires = ["uv_build>=0.8.13,<0.9.0"]
build-backend = "uv_build"
```

Except that broke things and the library wouldn't build or install once that was in. It turns out the `uv` maintainers think Python libraries should live in a `src` folder, not in the root directory, and so it kept looking for `src/feed_to_sqlite/__init__.py`, which doesn't exist.

[The fix](https://docs.astral.sh/uv/concepts/build-backend/#modules) is to tell `uv` to stop looking there, like this:

```toml
[tool.uv.build-backend]
module-root = ""
```

Now the library builds. Can I run tests?

My old setup had an optional test dependency, so I could use `pip install feed-to-sqlite[test]` to get the library and `pytest` installed. In `pyproject.toml`, that gets added like this: `uv install --group test pytest`, and then installed by running `uv sync --group test` or `uv sync --all-groups`. I don't know if there's a less verbose version. Mostly this happens in Github Actions, so it doesn't matter.

The last step was publishing this new version of the library.

Most of this was updating my `publish.yml` workflow. I'm also slowly switching my libraries over to use PyPI's [Trusted Publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/) system, which negates the need to manage credentials.

The one hiccup there was that I hit a permissions error a few times. I finally traced it to a missing `permissions` block in the workflow. Adding this block to the `deploy` job fixed it:

```yaml
permissions:
  id-token: write
```

I don't fully understand what that does. The only reference to it I found was in the [`actions/deploy-pages`](https://github.com/actions/deploy-pages) workflow. (Shoutout to Simon Willison for [opening an issue](https://github.com/actions/deploy-pages/issues/329) to ask about it.) But that solved the problem.

Since I got this migrated, I've closed a couple longstanding issues, and I have more fixes planned. This is all going toward another side project that I haven't actually started yet.
