---
title: So you want to build something interactive for your news story?
summary: Answer these questions before you start coding up that sweet new thing.
---

I've built a lot of interactive stories, and I've set up templates and storytelling infrastructure at a few news organizations. These are the questions I think need to be answered before building any bespoke storytelling experiences in-house.

## Where do you put your stuff?

In most cases, this is a bundle of files -- HTML, CSS and JavaScript -- that you can serve with something fast. The simpler that bundle is, the more options you have.

Object storage -- [Amazon S3](https://aws.amazon.com/s3/), [Google Cloud Storage](https://cloud.google.com/storage) or Microsoft's [Azure Blog Storage](https://azure.microsoft.com/en-us/products/storage/blobs/) -- remains a popular choice, especially if you don't need a URL that matches your main website. It's cheap, has basically infinite capacity and rarely fails.

Store your stuff there, and ideally put a CDN in front of it, and you're done. I've done this almost everywhere I've worked and never regretted it.

That said, there are other options, and sometimes other needs.

Static files are easy to serve, and if you're not doing [break the internet](https://www.merriam-webster.com/words-at-play/break-the-internet) traffic, you can probably use just about any off-the-shelf webserver.

How do I know this? Because in 2010, I built a [little ticker](https://www.pbs.org/newshour/nation/gulf-coast-oil-leak-widget) tracking the [Gulf Coast oil spill](https://www.pbs.org/newshour/tag/gulf-oil-spill) and it ended up on some of the most popular news sites in the world. We served it out of the static file directory of our little Movable Type instance.

Generally speaking, it's going to be easier to get files onto S3 or Cloud Storage than it would be to set up a server and run NGINX or Apache. But if that's your only option, it can work.

### Do I need a server?

Sometimes, yes, you do need a server. Maybe you need authentication, or your data is too big or too complicated to serve as static files, or you have a private API and need to mask it somewhere. Now what?

This is going to be more complicated than any of the options above. In most cases, I recommend a platform-as-a-service provider. I've used [Heroku](https://www.heroku.com/) for years, but lately all my side projects go on [fly.io](https://fly.io/). There are other options like [Netlify](https://www.netlify.com/) and [Vercel](https://vercel.com/).

These are going to vary widely in what they offer, what they cost and how much time you'll need to spend managing them.

If you get to this point, you are definitely doing [Product](https://chrisamico.com/blog/2023-02-01/three-kinds-of-code/). Remember to pay your (technical) debts.

## How do you get it there?

Deploying code to production (and to staging!) should be boring. It should be routine. Ideally, it shouldn't even require a developer.

Consider [this project](https://www.usatoday.com/storytelling/database-rating-dam-condition-climate-change-heavy-rain/) I worked on at USA TODAY. I wrote most of the code, but there were frequent updates as my colleagues tweaked copy and I touched up the design. Most of those updates used a Github Action that followed a standardized deployment process:

1. Clone a repository
2. Install dependencies
3. Pull data from Google Sheets, and possibly other places
4. Compile and render a [Svelte](https://svelte.dev/) application
5. Push the built files to Google Cloud Storage
6. Purge a frontend cache

On my old team, that process was so routine we rarely thought about it, but it enabled everything else we did. It completely took away the mental overhead of deployment.

## How does it get on your website?

Every CMS is a special snowflake, and there's no solution I can offer that's going to work everywhere.

- Can you put an `iframe` in a regular story?
- Do you have a special/longform/interactive story template?
- Can you inject HTML, CSS or JavaScript into story pages?
- Can you create blank pages with custom, maybe external assets?
- Or does anything that's not a story live on a subdomain?

How you answer the questions above will tell you how to get your cool interactive thing onto your website. And if you can't answer this question, you might need to rethink your storytelling choices.

## Who can update what?

This is an editorial question, not a technical one. You need to decide who is responsible for anything that might need to be changed, and how that's going to happen.

It's easy to fall into the trap of thinking words are for editors and everything else is for developers. But this whole thing is an editorial project, and everyone involved is a journalist. For example, the [last map in this story](https://www.azcentral.com/in-depth/news/2021/11/20/us-forest-service-water-management-limited-oversight-diversions/8446212002/) animates lines that trace water diversions. The text in each step lives in a spreadsheet, but there are also variables that let an editor change the speed of the animaation or the color of the lines. Changing those was an editorial choice, so those decisions lived in a place an editor could update if needed.

## Do you need to build anything?

Maybe not. There are great off-the-shelf tools that didn't exist a few years ago. I use [Felt](https://felt.com/) for maps and [Datawrapper](https://www.datawrapper.de/) or [Flourish](https://flourish.studio/) for charts. Don't sleep on good photos, video or illustration.

Before you go beyond those, make sure have an answer to the questions above.
