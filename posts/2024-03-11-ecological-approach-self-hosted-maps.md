---
title: An ecological approach to self-hosted maps
summary: We're working in a fast-changing space where solutions aren't stable, so it's important to take a problem-first approach.
---

At [NICAR 2024](https://www.ire.org/training/conferences/nicar-2024/), I taught a session on my approach to [self-hosted maps](https://chrisamico.com/blog/2024-02-13/self-hosted-maps/). While I wanted to give people a [practical set of tools](https://github.com/eyeseast/self-hosted-maps-codespace) to get a map built now, I stressed both during the class and in conversations throughout the conference that this is an evolving ecosystem, and the tools we're using this year might not be what we use a year or two from now.

I'm trying to build an ecological approach to self-hosted maps.

To understand how I got here, I need to talk about my main hobby: submission grappling and Brazilian jiujitsu. Don't worry, this will connect back to maps and journalism.

For about a year now, I've been exploring [ecological dynamics](https://www.primalmke.com/blogs/news/wtf-is-ecolgical-dynamics-a-gentle-onboarding) as a way to train [Brazilian jiujitsu](https://chrisamico.com/blog/2023-12-26/jiujitsu-gi-nogi/). At its core, I often describe this method as a _problem-first approach_, as opposed to a _solution-first approach_. Instead of focusing on specific moves, I try to think about the problems I need to solve in a specific situation and then repeatedly attack those specific problems.

For example, instead of learning a particular throw or takedown in isolation, I might play a game where I'm only trying to get inside my partner's grips and maintaining that advantageous position, without going further, and exposing both of us to all the little unnamed variables that come with grip fighting.

We repeat the problem, not the solution. Solutions aren't stable, so the idea is to become better at recognizing a problem and making the myriad unconscious adjustments necessary to solve it. (To see what this looks like, watch the [foundations class at Standard Jiu-Jitsu](https://www.youtube.com/watch?v=V4QtQTRwwD0), one of the most prominent advocates of the ecological approach.)

Anyone who has written javascript for a more than a few years will probably read "solutions aren't stable" and hear a ring of familiarity. How did we build websites a decade ago? Probably with [jQuery](https://jquery.com/), maybe with [Bootstrap](https://getbootstrap.com/) or another framework. Then there was [React](https://react.dev/), and later [Vue](https://vuejs.org/) and [Svelte](https://svelte.dev/) and a dozen other component frameworks. We choose build systems, formatters and linters, even flavors of javascript and CSS. It's a lot.

Building maps presents a consistent set of problems, even as the solutions have changed over the years. Indeed, last year at NICAR, Evan Wagstaff taught a [workshop](https://docs.google.com/presentation/d/1H9S_1h4-ezYZ0ixaUG_zPne1ufkk3prai-XXOKA1Pxc/edit#slide=id.p) on self-hosted maps with a workflow built around [Planetiler] and [Fly.io]. I expect someone could teach a mapping class at NICAR 2025 and there will be a different set of tools.

I want people who make maps on the internet to be able to adapt to this changing landscape. If a new tiling system appears tomorrow, I want you to understand how it might fit into your stack. If a tool you're using becomes unstable or outdated or you just don't like it anymore, I hope you know enough about the problem it's solving to find a replacement.

Go back to [my post about self-hosted maps](https://chrisamico.com/blog/2024-02-13/self-hosted-maps/), and you'll see that it's really just a list of problems you'll need to solve. Here they are again, rephrased as questions you'll need to answer:

- Where do I find data?
- How do I turn that data into tiles?
- How do I render those tiles in a browser?
- How do I style a map?
- How do I generate fonts and icons for a map style?
- How do I host and serve a finished map?

The way you answer those questions today probably won't be the same a year from now. That's OK. You can't step in the same river twice.

## Try it now

If you've read this far and you want to make a self-hosted map _today_, I do have something for you. I built [codespaces] on Github with map-tiling dependencies already built.

- [PMTiles + Tippecanoe + Vite + Datasette](https://github.com/eyeseast/self-hosted-maps-codespace): This is what I used in my session. In a few `make` commands, you'll have tiles, fonts and a basic map of Baltimore and all its public trees. I included a basic [Datasette] setup so you can query the tree data independent of the map.
- [Tilemaker + starter data](https://github.com/eyeseast/tilemaker-map-template): This should get you started with [tilemaker], including the [Natural Earth] data you'll need to render coastlines and populated places.

Both of these are template repositories, so clone them and use your own data or styles.

[planetiler]: https://github.com/onthegomap/planetiler
[fly.io]: https://fly.io/
[codespaces]: https://github.com/features/codespaces
[tilemaker]: https://github.com/systemed/tilemaker
[datasette]: https://datasette.io
