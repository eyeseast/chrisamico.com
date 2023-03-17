---
title: Boston parcels, mapped three ways
summary: The age of buildings, residential assessments and value density.
---

I made a few maps this week, just for fun, using Boston's parcel and assessment data.

All of these used my [Datasette GIS stack](https://github.com/eyeseast/spatial-data-cooking-show) to filter and join the relevant data and [Felt](https://felt.com) to visualize it.

### Age of Boston's buildings

Assessments include a column called `YR_BUILT` (and also a `YR_REMODEL` which could be interesting). Joining this to parcel boundaries gave me a map of Boston's buildings colored by age. Darker purple is the oldest parcels, and some go back to the 1700s. It's an old city.

<iframe width="100%" height="450" frameborder="0" title="Felt Map" src="https://felt.com/embed/map/Boston-buildings-colored-by-year-built-sPYjj6I0ROmOhnJ9AC9AURWD?lat=42.313051&lon=-71.068934&zoom=11.76"></iframe>

### Value of residential units

I initially made a map of [all property values](https://felt.com/map/Boston-buildings-Assessment-value-ePQe7WgaTgmjmbUmBOx9CwC), but that isn't very interesting when you include houses and also universities and an airport. Those big public works are expensive.

But filtering out [everything but residential units](https://github.com/eyeseast/boston-parcels/blob/main/queries/boston/residential-value.sql) -- coded as `R1`, `R2`, `R3`, `R4` and `CD` -- makes for an intersting map.

There are still things missing here: Mixed use buildings are a separate category, as well as large apartment buildings. I wanted to map places an individual might realistically own.

<iframe width="100%" height="450" frameborder="0" title="Felt Map" src="https://felt.com/embed/map/Boston-parcels-Residential-assessed-value-efGgl9AsxSMuMGp2tcdHmLB?lat=42.312442&lon=-71.085013&zoom=11.82"></iframe>

### Value density

While I was working on this, Jeffrey Baker in the [Felt community Slack](https://felt.com/community-signup) posted a map of [Alameda County](https://felt.com/map/Alameda-County-Parcels-2022-iNHItlavRg2zSCF4ncl9ACD), CA, colored by "value density," or assessment value divided by area. It's a smart way to handle the problem I had with the range of values in Boston.

Is it a huge surprise to see more concentrated land value downtown? No. But it's an interesting way to look at the city, and to think about the economic tradeoffs of living on its edges.

<iframe width="100%" height="450" frameborder="0" title="Felt Map" src="https://felt.com/embed/map/Boston-2023-value-density-x9Aa76bcdRm9BTPUr2kv9ADuD?lat=42.31251&lon=-71.05698&zoom=11.75"></iframe>

All the code I used is [here](https://github.com/eyeseast/boston-parcels). Open an issue if there's something you'd like to see mapped.
