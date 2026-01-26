---
title: Migrating a large codebase to Svelte 5 in small steps
summary: Is this like eating an elephant?
---

Just over a year ago, a new version of DocumentCloud rolled out, running on SvelteKit. Specifically, it ran on Svelte 4, despite Svelte 5 landing right as we were ready to launch.

DocumentCloud is a big, complicated codebase, and it has lots of dependencies. We spent a year making other improvements before finally upgrading to Svelte 5 at the start of 2026. But upgraing is one thing, and migrating is another.

Svelte 5 introduced a new state management syntax -- runes -- alongside other changes that generally make the whole codebase stricter about typing. I'm fine with this. There was a moment of panic -- slots are gone? events are different? `$props()`? -- but after using Svelte 5 on smaller projects, it's honestly a better system. There's just less room for error.

In much the same way as Go made me a fan of strict types in general, DocumentCloud and Svelte have convinced me to appreciate TypeScript.

## Small bites

The Svelte CLI has a one-shot migration tool that will ugprade and transform an entire codebase:

```sh
npx sv migrate svelte-5
```

What it does:

> Upgrades a Svelte 4 app to use Svelte 5, and updates individual components to use runes and other Svelte 5 syntax (see migration guide).

That is ... a lot. Maybe it's fine on a small codebase, but there was no way I was going to run that against DocumentCloud. For one thing, we had conflicting dependencies. And also, some components won't migrate automatically.

Fortunately, Svelte 4 components still work. We upgraded our dependencies, upgraded to Svelte 5 and deployed. And then we started migrating components in small groups.

## Mixing syntax

One of the big changes in Svelte 5 is the deprecation of `<slot>` for composition. This was a relic of web components, which were definitely going to be a thing until everyone moved on. Because this is javascript.

Svelte 5 uses `{#snippet thing()}` and `{@render thing()}` to [pass through chunks of markup, and optionally data](https://svelte.dev/docs/svelte/v5-migration-guide#Snippets-instead-of-slots).

This is, honestly, a better system. But what if I haven't migrated all of my components in my giant codebase?

It turns out, you can use both. We have lots of components that use `<slot>`, and those still work in updated components. Where we've migrated a child component but not a parent, we can use `{#snippet ...}`

The same is true of state and stores. SvelteKit switched from a `$page` store to a `page` state object. Both work in runes or legacy mode, so we can migrate incrementally.

## Living in two worlds

I'm in the middle of this migration as I write this, and I don't know when it'll be done. Backwards compatability is great, but it creates the temptation to live in two worlds.

But Ian Malcolm was right: Just because you can, you need to think about whether you should. The longer we sit in between Svelte 4 and 5, the more we have to deal with two syntaxes instead of one.
