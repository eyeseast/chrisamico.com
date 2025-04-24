---
title: How I'm using AI now
summary: This is true as of April 2025. It'll probably be different a month from now, and definitely a year from now.
---

Large language models have become so ubiquitous so quickly that it's easy to forget how new they are. I still feel like I'm barely up to speed, but I have friends who are using them daily. And the more I poke at them, the more I use them, so I want to document how I'm using them now.

## Asking questions, getting examples

The main thing I've been doing, mostly with Claude and ChatGPT, is asking questions about code. I have a little side project where I want to record audio from a web browser, but I've never done that, so I asked Claude how it works.

> I’m building a web application that will let users record themselves reading a short text passage. I want the user to record a short audio file and save the file to cloud storage.

Claude built an entire React app to answer the question. I poked around, asked to see a SvelteKit version, tweaked things. I don't know if I'll use any of it, but it's useful just to see how it works.

In another thread, I asked about using Postgres in SvelteKit, because I've never done that. It gave me a bunch of library choices. Could I have answered this question with a Google search and Stack Overflow? Definitely. But this is an easier way to put the pieces together.

## Lists of things

When Joe Biden dropped out of last year's presidential election and Kamala Harris became the Democratic nominee, I realized she might be the closest candidate to my age (at the time of the election).

Curious if this was true, I asked Claude for a list of all major party nominees and dates of birth. A few rounds of prompts later, I had [a spreadsheet](https://docs.google.com/spreadsheets/d/1e1e2NVWa6oyxJd7pmOuzdrjYFjUK20gmLNJqB7MmREU/edit?gid=0#gid=0), which I could easily check against other sources.

I did something similar when I was curious about [long-running movie francheses](https://chatgpt.com/c/f98431e9-53f1-429b-b15d-5b4fd09a496f). In this cases, I used ChatGPT. Once I had a format I liked, I just gave it new franchises as I thought of them. That all went into [another spreadsheet](https://docs.google.com/spreadsheets/d/1-aQKtCux1y_cUAi8fowWuf19UPDNFEDv1WTJFEq0OqY/edit?gid=0#gid=0).

One thing I learned on that little side project: I needed a way to quickly see if an LLM is hallucinating, so I asked ChatGPT to include an IMDB link for each movie. A few of those URLs didn't lead anywhere, because ChatGPT had invented sequels. That was a good low-risk lesson.

## Translations, in production

I have one place I've used an LLM in production: generating translations for DocumentCloud.

When we [rebuilt DocumentCloud's front end](https://www.muckrock.com/news/archives/2024/oct/08/a-new-documentcloud-is-coming-try-it-now/) last year, most of the site's existing translation strings became obsolete.

I wrote a [small Python script](https://github.com/MuckRock/documentcloud-frontend/blob/main/utility/translate.py) to take each string from the site's [JSON file for English text](https://github.com/MuckRock/documentcloud-frontend/blob/main/src/langs/json/en.json) and run each line through Ollama, using [Llama 3.2](https://ollama.com/library/llama3.2).

I wanted to use a local model for this, because I was sending each string individually and figured that would be faster. I also wanted to keep costs down.

This took [more prompt iterations](https://github.com/MuckRock/documentcloud-frontend/commits/main/utility/translate.py) than I expected, especially around dealing with format strings. But we got there, at least for the romance languages. It helped that I can read Italian and muddle through Spanish and French (especially with Google Translate to help). German, Russian and Ukranian will need a different approach, or a different model, but this is a start.
