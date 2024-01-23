---
title: Mapping wildfires with Datasette and Felt
summary: The tools are getting better and the fires are getting worse.
---

It's a testament to how bad 2020 was that I barely remember the wildfire season, which was the worst in at least 40 years. Friends in the Bay Area complained about being stuck inside to avoid the horrific air quality, and thousands were evacuated to shelters while the COVID-19 pandemic peaked.

Yet an EPA rule could allow that smoke to be excluded from official pollution records, as my [colleagues reported](https://www.muckrock.com/news/archives/2023/may/23/wildfire-smoke-exceptional-event/):

> Over the last three decades, the number of acres burned by wildfire has grown, spewing smoke across California and the country. The new GAO report highlights how a loophole in the Clean Air Act permits the EPA to erase pollution — not from the sky, but from the record.
>
> The tool for erasing some of the worst air-pollution days is called the “exceptional events” rule — a legal pathway that allows local regulators to make a case that air pollution from “natural” wildfires shouldn’t count against their federal air quality goals.

As part of that story, I mapped and charted 40 years of wildfires using data from the [National Interagency Fire Center](https://data-nifc.opendata.arcgis.com/datasets/nifc::interagencyfireperimeterhistory-all-years-view/about).

<iframe
  src="https://muckrock.github.io/wildfires-protomaps/#3/40.48443/-104.777596"
  width="100%"
  height="450px"
  frameborder="0"
  title="Wildfires: 1980 - 2021"
></iframe>

I recommend looking at the map on the biggest screen you can, and zooming into a place you know. You can filter the map to show one decade at a time, and the change is shocking in some places. [Sonoma County](https://felt.com/map/Wildfires-are-becoming-more-frequent-across-the-West-QBFznerjRpK6BWnGzY9BRYC?lat=38.574223&lon=-122.029378&zoom=9.29) is a good place to start.

<div><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/EjL0r/embed.js?v=4" charset="utf-8"></script><noscript><img src="https://datawrapper.dwcdn.net/EjL0r/full.png" alt="A line chart shows the increase in acres burned by wildfire in the United States between 1980 and 2021. Faded bars in the background show individual years, while a three-year average shows the overall trend." /></noscript></div>

I used [Datasette](https://datasette.io/) and my [SpatiaLite stack](https://github.com/eyeseast/spatial-data-cooking-show) to analyze fire data. The code is [available on Github](https://github.com/MuckRock/gao-wildfire-exceptions). A few libraries really helped:

- [geojson-to-sqlite](https://github.com/simonw/geojson-to-sqlite) loads GeoJSON into a SQLite database
- [datasette-geojson](https://github.com/eyeseast/datasette-geojson) adds GeoJSON output to Datasette
- [datasette-geojson-map](https://github.com/eyeseast/datasette-geojson-map) renders a map for geographic queries
- [datasette-query-files](https://github.com/eyeseast/datasette-query-files) lets me write canned queries as SQL files

I can't say enough how useful it is to be able to ask a question, write a SQL query and see a map. Once I had a version version I liked, I downloaded the GeoJSON version of the same query and plugged it into [Felt](https://felt.com) and styled an interactive map.

For the chart, I wrote grouped and summed fires by year and added a [three-year rolling average](https://github.com/MuckRock/gao-wildfire-exceptions/blob/main/queries/wildfires/acres-burned.sql). I exported that as a CSV file and plugged it into [Datawrapper](https://datawrapper.de).

Coding the map and chart by hand probably would've taken me a day, and they might not have looked as nice. I also would've needed [hosting infrastructure](https://chrisamico.com/blog/2023-05-20/interactive-app-infrastructure/), which I haven't yet set up at MuckRock (and maybe I never will). Instead, I had drafts of each visual in front of editors in less than half an hour.

---

**Update**: I had to rebuild the map by hand after Felt started requiring paid plans to embed maps. I'll write more about how I built this new version in a later post. The original map is still on [Felt](https://felt.com/map/Wildfires-are-becoming-more-frequent-across-the-West-QBFznerjRpK6BWnGzY9BRYC?lat=38.574223&lon=-122.029378&zoom=9.29).
