---
title: Archiving needs to be a regular part of publishing
summary: Archive the inputs. Archive the outputs.
---

We live in an unfortunate era of disappearing culture.

This week, FiveThirtyEight became the latest news site to be shut down and turned off, its old URL redirecting to the ABC News politics archive. A site that changed political coverage in the United States and beyond is just gone. Former staffers now looking for new jobs can't even link to their old work. This is both a tragedy and unnecessary cruelty by a media conglomerate that wouldn't even notice the hosting costs on its balance sheet.

It's also a [familiar story](https://www.muckrock.com/news/archives/2024/mar/06/for-the-record-the-battle-to-preserve-the-online-archives-of-now-shuttered-newsrooms/).

Late last year, my old employer, Gannett, flipped a switch and five years of my own work disappeared. The former Storytelling Studio, where I was a senior developer, built tools used by hundreds of journalists across that chain's network of 200 newspapers. Our flagship product, the In Depth framework, gave newsrooms the ability to create unique and bespoke story layouts without relying on a developer writing new code. More than 8,000 stories used In Depth over five years. Now it's gone.

At the same time, the federal government has begun an [unprecedented purge of public data](https://www.muckrock.com/news/archives/2025/feb/04/the-fight-to-preserve-federal-government-data/) and information. Sources that journalists relied on for decades are disappearing, often without warning.

What do we do about this? How should journalists think about this new era?

Archiving needs to become a standard part of our publishing process. We should be saving our inputs and outputs, and documenting as we go. We should be working across organizations to preserve public information, and we should help our audiences find what has been saved. We should also be cleareyed and plainspoken about what has been deleted, and why.

## Archive the inputs

A story that relies on public data should also archive that data, in a place separate from its original source and safe from deletion.

This hasn't been my habit for most of my career, but it will be now. If I'm mapping something from Census data, I'm going to snapshot that data and save it with my code. If I'm reporting for documents, of course, they're going in [DocumentCloud]. I'm also going to start pushing documents to [IPFS](https://www.documentcloud.org/add-ons/MuckRock/documentcloud-filecoin-addon/).

I need to think through how I'm going to organize all of this, because I can't keep a local copy of the US Census. [NHGIS] and [CensusReporter] are already doing great work in this area, and I'm going to rely on them more than I already do.

I'm also watching more public pages for potential deletion, using [Klaxon]. I don't know what I'll need in the future, so this is a precaution.

## Archive the outputs

When I left Gannett, I sent a list of In Depth URLs and projects I'd worked on to the Internet Archive, because I (correctly, it turns out) didn't trust the company to take care of my stuff.

But this shouldn't be a one-off, frantic process in an already-stressful time. It needs to be part of publishing.

Sending a URL to the Internet Archive is easy. Put a link in [Save Page Now](https://web.archive.org/save/) and it's done. Or do it from the command line, using Ben Welsh's [excellent tool](https://github.com/palewire/savepagenow).

Do this the moment you hit publish. I'm going to add a step to the publishing process for this site to run `savepagenow` for each blog post I publish. There's no reason to wait.

## Work together

Archiving is a practice. Library science is a field of study. There are people in the world who are good at this, and who have been working on preserving the internet for decades. These are critical partners for journalists now.

Some starting points:

- [End of Term Archive](https://eotarchive.org/)
- [Internet Archive](https://archive.org/)
- [Harvard's Library Innovation Lab](https://lil.law.harvard.edu/)
- [MuckRock](https://www.muckrock.com) and the [Data Liberation Project](https://www.data-liberation-project.org/)

MuckRock ran a webinar on this recently:

<iframe width="100%" height="415" src="https://www.youtube-nocookie.com/embed/hiZuKA-o4V4?si=vHnVwNQU6k9La8o0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

This is part of the work now. The internet isn't going to preserve itself.

_Disclosures: I work for MuckRock and DocumentCloud is my main project. I'd say all this anyway. It's why I work there._

[DocumentCloud]: https://www.documentcloud.org
[NHGIS]: https://www.nhgis.org/
[CensusReporter]: https://censusreporter.org/
[Klaxon]: https://www.documentcloud.org/add-ons/MuckRock/Klaxon/
