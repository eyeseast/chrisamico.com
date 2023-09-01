---
title: The Three Kinds of Code You Write in the Newsroom
summary: And there are only three.

style: |
  .team {
    display: flex;
    margin: 0 auto;
    width: 100%;
  }

  .box {
    border: 5px solid black;
    margin: 20px;
    padding: 20px;
    text-align: center;
  }

  .skills li {
    display: inline-block;
    padding: 5px;
  }
---

_This is a [lightning talk](https://rjionline.org/news/the-three-kinds-of-code-you-write-in-the-newsroom/) I gave at NICAR 2020. Since then, this framework has become the primary way I explain what programmers (like myself) do in newsrooms. You can watch a video of the talk [here](https://youtu.be/TwJhJ44mTuE) or click through slides [here](https://eyeseast.github.io/nicar-2020-three-kinds-of-code/)._

A couple years ago, I had one of those opportunities you don't get often: I got to build a team from scratch.

Not a big team, there would be three of us, and we'd have a role in basically everything that required code on a small news site -- from [data journalism](https://www.pbs.org/wgbh/frontline/interactive/child-marriage-by-the-numbers/), to [experimenting with new story forms](https://www.pbs.org/wgbh/frontline/interactive/inheritance/), to a [major site redesign](https://www.pbs.org/wgbh/frontline/article/welcome-to-our-new-site/).

<figure>
    <div class="team">
        <span class="box">
        ??
        </span>
        <span class="box">
        me
        </span>
        <span class="box">
        ??
        </span>
    </div>
</figure>

As we got into the hiring process, I started making a list of all the skills we might need, so I could compare candidates.

<figure>
    <ul class="skills">
        <li>html</li>
        <li>css</li>
        <li>javascript</li>
        <li>php</li>
        <li>sql</li>
        <li>python</li>
        <li>git</li>
        <li>node</li>
        <li>d3</li>
        <li>photoshop</li>
        <li>illustrator</li>
        <li>wordpress</li>
        <li>excel</li>
        <li>R</li>
        <li>foia</li>
        <li>statistics</li>
        <li>scraping</li>
        <li>bash</li>
        <li>video editing</li>
        <li>after effects</li>
        <li>dev ops</li>
        <li>mapping</li>
        <li>...</li>
    </ul>
</figure>

This got overwhelming pretty quickly.

I didn't realize it at the time, but this was part of a problem I'd been struggling with in different ways since I started writing code for journalism, back when George W Bush was still president.

It's a problem of language.

<figure>
    <img src="https://upload.wikimedia.org/wikipedia/commons/0/09/Turris_Babel_by_Athanasius_Kircher.jpg" alt="Turris Babel by Athanasius Kircher.jpg" height="467" width="480"></a>
    <figcaption>By <a href="https://en.wikipedia.org/wiki/en:Coenraet_Decker" class="extiw" title="w:en:Coenraet Decker"><span title="Dutch Golden Age engraver">Coenraet Decker</span></a> - <a rel="nofollow" class="external free" href="http://digi.ub.uni-heidelberg.de/diglit/kircher1679/0059">http://digi.ub.uni-heidelberg.de/diglit/kircher1679/0059</a>, Public Domain, <a href="https://commons.wikimedia.org/w/index.php?curid=35102210">Link</a></figcaption>
</figure>

There's an overwhelming number of skills and tools we use in writing code around news.

Most of those, and most job descriptions, are lumped together into titles like "news applications" or "interactives" or data journalism.

Then a few months ago, a friend asked me to talk to one of her students who was a talented photographer and also starting a comp sci program. And he wanted to know what to do with that set of skills.

And after talking to him and thinking about the jobs I've had, I realized that ultimately, there are three kinds of code we write in newsrooms:

**Reporting**. **Storytelling**. **Product**.

And that's pretty much it.

So what do I mean by reporting, storytelling and product?

**Reporting** code is, well, reporting. It's how we gather information and ask questions of it. It's scraping, data analysis, machine learning and natural language processing. When you're using SQL, R, Pandas and Jupyter notebooks, you're probably writing code I'd call reporting. If you're writing code to figure out if you have a story, I'd say you're doing reporting.

**Storytelling** is, of course, what we do with all that reporting. It's our graphics, interactive or not, and maps and charts and generative text. It's AR and VR and 3D modeling. We know what we're trying to say, because we did the reporting, and now we're speaking with code.

And what is product? You might be thinking: We have another department that does that. They build the CMS and handle ad code, and I'm in the newsroom.

And I'm here to say, _more of us are doing product than we realize_.

**Product** is everything we build that isn't for just one story or project.

It's everything we do between deadlines that makes our next project launch faster or run smoother or get a little closer to what our audience needs. (In fact, it's everywhere we talk about user needs.)

It's anything we need to maintain, and anything that accumulated technical debt. (You might say it is the technical debt.)

It's our app templates and starter kits that we update after we launch a project. It's our longform tool. It's our open source code. It's our analytics packages and documented best practices.

## An example: Ahead of the Fire

[Here's an example](https://www.azcentral.com/in-depth/news/local/arizona-wildfires/2019/07/22/wildfire-risks-more-than-500-spots-have-greater-hazard-than-paradise/1434502001/). This series -- [Ahead of the Fire](https://www.azcentral.com/in-depth/news/local/arizona-wildfires/2019/07/22/wildfire-risks-more-than-500-spots-have-greater-hazard-than-paradise/1434502001/) -- looked a wildfire risk across the Western United States.

In the reporting phase, my colleagues used GIS tools to ask which communities are most at risk, and which particular risks does each community face.

The storytelling side focused on explaining those risks and the methodology behind the story.

And here's product: We call this the In-Depth framework, and it's the machinary that powers our best storytelling.

So why does it matter what we call these kinds of code? Because they move at different speeds. And every newsroom I've worked in has struggled at moving at different speeds.

![chart of reporting, storytelling and product cadence](https://media.githubusercontent.com/media/eyeseast/nicar-2020-three-kinds-of-code/main/assets/code-speeds.png)

Think of a project you worked on that went well. It probably started with a lot of reporting, which tapered off as the story solidified and you started to focus on storytelling. Meanwhile, product is (or should be) moving along in a steady cadence of sprints.

And this is where it's important to know what kind of code we're writing, and to be able to talk about it with other people in the newsroom, especially our editors. This is where it's easy to screw things up.

This is where I've screwed things up.

Like trying to make something reusable too early: I wrote [a Python client for the ProPublica Congress API](https://github.com/eyeseast/propublica-congress) because someone pitched a story related to Congress, and my response was to create a library. Cool. Never used it for a story.

Or falling in love with storytelling when it's time to move into product: [This story on Zika](http://apps.frontline.org/zika-water/) was great. We did a dozen like it, with a little variation, each one basically a bespoke Tarbell project.

After about the third one, we really should have started building tools into WordPress, but I was nervous about technical debt. This is where it helps to think in product terms.

Writing storytelling code that becomes technical debt: The original topper [in this story](https://www.desertsun.com/in-depth/news/environment/border-pollution/poisoned-cities/2018/12/05/air-pollution-taking-deadly-toll-u-s-mexico-border/1381585002/) was gorgeous. It was also built into our storytelling framework, which meant we were responsible for maintaining it. Forever. Oops. (We finally made it a static image.)

I'm sure you have your own examples.

Thinking about these three distinct kinds of code can help beyond individual projects.

If you're looking at a job description, it's a good way to get a read on what kind of job it is, and whether it matches up with your skills or career goals. You might use it to decide which NICAR sessions to go to.

It helps answer the question: "Should I learn [fill in the blank]?"

Now you can reframe it as:

- "What is X best suited for?"
- "How might X be used for reporting, for storytelling, for product?"

One last thing:

When I talk about three kinds of code, I want to be very clear that I don't mean there are three kinds of coders.

As I said at the top, most of us are doing all three kinds of programming, and I think that's a good thing, because it pushes us to be better and more well-rounded, both as programmers and as journalists.

Reporting and storytelling are still the core of our profession, and product is going to open up new ways of doing both.

We all have a lot to learn from each other.
