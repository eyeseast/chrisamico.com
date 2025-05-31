---
title: Can Claude count cards?
summary: Or will I get cheated by ChatGPT?
---

Some friends brought over the game _Cover Your Assets_ last weekend for a game night with the kids. At the end of the first hand, everybody started counting at once, out loud, as kids do.

So I thought, Let's see how Claude does at scoring a hand. I took a picture, uploaded it to the app, and gave it a simple prompt: "Count the value of all of these cards, in dollars."

<figure><a data-flickr-embed="true" href="https://www.flickr.com/photos/chrisamico/54545788680/in/datetaken/" title="Cover your assets"><img src="https://live.staticflickr.com/65535/54545788680_5007897037_z.jpg" width="480" height="640" alt="A winning hand in the game 'Cover your Assets'"/></a>
<figcaption>Beginner's luck</figcaption>
</figure>

Claude's estimated total: "approximately $560,000."

Cool. I have the ChatGPT app on my phone, too, so let's try that with the same photo, same prompt. "So, the total value of the cards is $430,000," says the second robot.

That's interesting. I guess we better try more.

I used [llm](https://llm.datasette.io/en/stable/) and a little Python to loop through 21 OpenAI and Anthropic models that all support JPEG attachments. All the code is [on Github](https://github.com/eyeseast/llm-count-cards).

The results are all over the place, from $345,000 using `gpt-4.1-nano` to $545,000 using `claude-sonnet-4-0`. All of the individual results were in the repo, showing full responses and token usage.

I've been excited lately about the possibility of using AI and computer vision for reporting, and large language models can do amazing work in this space. But this was a good reminder that results need to be checked, and carefully.

The correct answer here is $465,000.
