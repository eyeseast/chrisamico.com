---
title: Who owns my stack?
summary: An end-to-end tour of the tech I'm using and who pays for it.
---

First things first: I'm typing this on a 2023 Macbook Pro, built by Apple. I own it.

You are reading this on my website, which I built. The source code is [on Github](https://github.com/eyeseast/chrisamico.com).

I own the domain, which I registered in Hong Kong back in 2007. At the time, that kept it close to where I was living -- Dalian, China -- while still outside the [Great Firewall](https://en.wikipedia.org/wiki/Great_Firewall). I should move it.

The site runs in [Python](https://www.python.org/), owned by the [Python Software Foundation](https://www.python.org/psf-landing/), a charitable foundation that oversees development of the language and core parts of its ecosystem. All of my [dependencies](https://github.com/eyeseast/chrisamico.com/blob/main/pyproject.toml) are open source and mostly maintained by volunteers. (Some are getting a little stale, though.) One is my longest-running open source project, [`python-frontmatter`](https://pypi.org/project/python-frontmatter/).

I wrote the CSS by hand, building on [normalize.css](https://github.com/necolas/normalize.css). There's no javascript.

From there, it gets more complicated.

I'm typing this post into VS Code, which Microsoft built. Microsoft also owns Github, where I host the code and the published site, via Github Pages.

And while this site has no javascript, almost everything else I build does, and Microsoft also owns a large chunk of that stack, specifically [npm](https://www.npmjs.com/), through Github, and [TypeScript](https://github.com/microsoft/TypeScript).

Back to this site: I save links in an SQLite database. SQLite is in the public domain, though there is a very small company being it, which offers [professional support](https://sqlite.org/prosupport.html). I use Simon Willison's [`sqlite-utils`](https://github.com/simonw/sqlite-utils) and [Datasette](https://datasette.io/) to manage that database (and have contributed code to both those projects).

I recently switched this site's build and dependency system from [`Pipenv` to `uv`](https://chrisamico.com/blog/2025-12-07/uv-new-python-setup/). [Astral](https://astral.sh/), maker of `uv` and other tools, recently [sold itself to OpenAI](https://astral.sh/blog/openai). Pipenv had its problems -- speed, mostly -- but ownership wasn't one of them. I worry less about the [Python Packaging Authority](https://www.pypa.io/en/latest/) going away than OpenAI losing interest in maintaining Astral's free tools.

In my day job, I work in Svelte, whose license points to its own contributors as copyright holders. Vercel officially backs the project, though, and [hired its lead author](https://vercel.com/blog/vercel-welcomes-rich-harris-creator-of-svelte), Rich Harris. (Rich did answer questions about Svelte's future and independence [at the time](https://www.reddit.com/r/sveltejs/comments/19ac6lp/concern_about_the_future_of_svelte/).)

Svelte (and especially [SvelteKit](https://svelte.dev/docs/kit/introduction)) is tied into [Vite](https://vite.dev/), which is part of [VoidZero](https://voidzero.dev/). And [VoidZero is now part of Cloudflare](https://voidzero.dev/posts/voidzero-cloudflare). I hope that's a good home.

Django is the other piece of my work stack, and also the first framework I ever learned. Thankfully, it seems safely housed in its own [foundation](https://www.djangoproject.com/foundation/).

Friends of mine have worried lately about giant companies buying projects they depend on, and I can't blame them, though I'm also not surprised. Open source projects with venture backing were probably always destined for acquisition. There's no other realistic way to get a return on free software.

Likewise, projects with a single lead developer or tiny core team are probably better housed at a company that can afford to subsize development. Setting up and running a foundation is hard, and it comes with its own overhead. Svelte was a side project while Rich Harris worked at the Guardian and New York Times, but Vercel can pay him to work on it full time. [Bun](https://bun.com/blog/bun-joins-anthropic) is in a similar position.

I don't have a better model to hand anyone. Squaring "software should be free" with "developers should get paid" is a hard problem.

But the risk is real, as everyone who used [Skype](https://en.wikipedia.org/wiki/Skype) can attest. The nature of software is churn, and the internet doubly so.
