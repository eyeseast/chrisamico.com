---
title: Cheap content is the least interesting way to use LLMs in journalism
summary: We don't need to be in the slop business, and we can use AI to solve real problems.
---

<figure>
<a data-flickr-embed="true" href="https://www.flickr.com/photos/chrisamico/54542966043/in/datetaken/" title="Stop hiring humans"><img src="https://live.staticflickr.com/65535/54542966043_bacb33403c_z.jpg" width="640" height="480" alt="A billboard over a freeway that says, 'Stop hiring humans'"/></a>
<figcaption>Is this the business news organizations want to be in?</figcaption>
</figure>

[Slop](https://simonwillison.net/2024/May/8/slop/) is a problem because slop is cheap. At least two news organizations fell into the cheap content trap this week. The Chicago Sun-Times ran a summer guide produced by Hearst full of [hallucinated book titles](https://www.niemanlab.org/2025/05/you-wont-find-these-on-the-shelf-newspapers-print-an-ai-generated-reading-list-with-fake-books/).

Cheap content will always be a temptation for news organizations that are saddled with debt and running with skeleton crews, even as it saps trust and produces embarassments. All of this has happened before, and all of it will happen again.

And yet, I believe journalists should continue exploring and investing in artificial intelligence. Producing cheap, filler content might be the least interesting way to use large language models in news. There are better uses for this technology.

NiemanLab [highlighted](https://www.niemanlab.org/2025/05/how-this-years-pulitzer-awardees-used-ai-in-their-reporting/) how some of this year's Pulitzer winners and finalists used AI:

> “At this early juncture, we see responsible AI use as a significant component in the increasingly versatile toolkit utilized by today’s working journalists,” said Marjorie Miller, the administrator of the Pulitzer Prizes, who also called attention to other tools represented among the winners, including statistical analysis, public record requests, and visual forensics. “[AI] technology, when used appropriately, seems to add agility, depth and rigor to projects in ways that were not possible a decade ago.”

Teams used AI for visualization, data extraction, categorization and visual analysis, all with human supervision.

Here are a few more things we might all try:

**Structured data extraction.** Derek Willis parsed and extracted [structured data from congressional job postings](https://thescoop.org/archives/2025/02/28/turning-congressional-job-listings-into-data/), using Google Gemini. "Oh, and cost? I’m cheap, so I ran this using Gemini’s 1,500 daily API calls on the free tier. Took me a few days. $0."

**Classification.** Derek and Ben Welsh taught a class at this year's NICAR conference on [building LLM classifiers](https://palewi.re/docs/first-llm-classifier/index.html). It's a great introduction to what the latest models can do.

**Personalized weather reports.** If you're going to generate cheap content, at least make it meaningful. Maybe even make it playful. Drew Breunig [built a fun weather reporter](https://www.dbreunig.com/2024/10/29/generating-descriptive-weather-forecasts-with-llms.html) with free data, open source tools and Github Actions. I forked it and [made my own](https://eyeseast.github.io/boston-weather-bot/).
