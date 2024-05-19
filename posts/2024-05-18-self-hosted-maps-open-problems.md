---
title: Not-yet-solved problems in self-hosted mapping
---

In my post on using [an ecological approach for self-hosted maps](/blog/2024-03-11/ecological-approach-self-hosted-maps/), I listed out a set of problems we need to solve any time we build a map on the internet:

- Where do I find data?
- How do I turn that data into tiles?
- How do I render those tiles in a browser?
- How do I style a map?
- How do I generate fonts and icons for a map style?
- How do I host and serve a finished map?

The good news is, these problems have [pretty good solutions](/blog/2024-02-13/self-hosted-maps/) as of 2024. The NPR Visuals team used the stack I presented at [NICAR in Baltimore](https://github.com/eyeseast/nicar24-self-hosted-maps) and built a guide to [the USDA's updated plant hardiness zones](https://apps.npr.org/plant-hardiness-garden-map/). It's an awesome project with a great map, localization and a great explanation of the close-to-home impact of climate change.

There are other mapping problems, though, that don't have ready solutions, or have solutions that may require project-specific decisions.

- Satellite images
- Terrain data
- Static map images
- Raster maps in general (supporting @leaflet for example)
- Directions
- Geocoding
- Legends and other bespoke controls

(I posted about this a while ago [on Mastodon](https://journa.host/@chrisamico/112128744346351870) and got a few answers.)

## Satellite images

[Mapbox Satellite](https://www.mapbox.com/maps/satellite) and Google Earth remain the best-in-class solution for satellite imagery. Getting a cloudless tileset for the entire planet is a monumental computing task.

I suspect a more practical approach for self-hosting will be to focus on a specific area and use tools like [landsat-util](https://pythonhosted.org/landsat-util/overview.html) and [rasterio](https://github.com/rasterio/rasterio) to process images into usable tiles.

## Terrain data

Hillshading and three-dimensional extrusions rely on terrain elevation data. [Mapbox has this](https://docs.mapbox.com/data/tilesets/guides/access-elevation-data/). Mapzen built and open-sourced [joerd](https://github.com/tilezen/joerd) to "to download, merge and generate tiles from digital elevation data," though the project hasn't been updated in seven years.

I've barely touched terrain data and <abbr title="Digital Elevation Model">DEM</abbr> files, so I'm not even sure where to start with this. But if we want to build 3D maps, we need a process to manage elevation data.

## Static map images

Sometimes, I don't want an interactive map drawn from vector data on a `canvas` element using WebGL. I want a static image of a fixed area that works without javascript. Maybe I even want to print it.

Maptiler's [tileserver-gl](https://github.com/maptiler/tileserver-gl) will turn vector datasets and [Maplibre styles](https://maplibre.org/maplibre-style-spec/) into raster tiles on the fly. I've used it to work on Leaflet maps on a cross-country flight. (That is, in part, how I started looking at self-hosted maps.)

It's also possible to [export](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob) the rendered contents of a `canvas` element as an image. This might be enough to build something like a locator map workflow.

## Raster maps and Leaflet support

While vector maps are fantastic, there are two cases where we still need raster tiles: satellite images and [Leaflet](https://leafletjs.com/) support.

Leaflet is an older mapping engine than Mapbox or Maplibre. Leaflet _can_ handle vector tiles using [protomaps-leaflet](https://github.com/protomaps/protomaps-leaflet), but even that project states up front that it's mostly a gap-filler:

> New projects starting from scratch should probably use MapLibre GL, but this library is useful as a drop-in replacement for raster basemaps in Leaflet, either using the Protomaps API or PMTiles on your own storage.

The core problem is that generating and storing millions of image tiles is slow and expensive. If you need to render a street map using image tiles, running Maptiler's [tileserver-gl](https://github.com/maptiler/tileserver-gl) is probably the best solution. Be sure to put it behind a caching proxy so you're not regenerating image tiles constantly.

Another project I need to look into: [TiTiler](https://developmentseed.org/titiler/), which turns [cloud-optimized geotiffs (COGs)](https://www.cogeo.org/) into tiles on the fly. This is another problem I haven't needed to solve yet, but maybe you have. To see it in action, check out [OldInsuranceMaps.net](https://oldinsurancemaps.net/) and read [this writeup on Development Seed](https://developmentseed.org/blog/2023-12-01-spotlight-oldinsurancemaps).

## Directions and Isochrones

We all use Google Maps and Apple Maps and Waze for directions. What can we host ourselves?

[Valhalla](https://valhalla.github.io/valhalla/) seems to be the best open source solution for generating directions using OpenStreetMap data. I haven't tried it, yet, but I will at some point.

Valhalla can also generate [isochrones](https://valhalla.github.io/valhalla/api/isochrone/api-reference/), which could be especially useful in stories about transportation.

Another service worth looking at: [openrouteservice](https://openrouteservice.org/). It offers an API for both directions and isochrones, and it can be [self-hosted](https://github.com/GIScience/openrouteservice).

## Geocoding

Turning addresses into mappable points is a regular part of reporting and visualization. Hosted services like Google and Mapbox are expensive and have restrictive terms of service, like requiring you to use the returned data on a map.

I've been using [OpenCage](https://opencagedata.com/) for a while. It lets you bulk geocode, store the results and use them anywhere.
If you're using [Datasette](https://datasette.io), you can use it with [geocode-sqlite](https://github.com/eyeseast/geocode-sqlite) (which I wrote) or [datasette-enrichments-opencage](https://datasette.io/plugins/datasette-enrichments-opencage).

When I asked about self-hosted geocoding on Mastodon, Brandon Liu of Protomaps [recommended](https://journa.host/@protomaps@mapstodon.space/112133736230737208) Pelias, [Photon](https://github.com/komoot/photon) and [Airmail](https://github.com/ellenhp/airmail). Those last two were new to me, so I can't say much about them, but it's good to see new approaches emerging.

[Pelias](https://pelias.io/) is probably the most mature self-hosted geocoding solution. It grew out of [Mapzen](https://www.mapzen.com/) and lives on at [geocode.earth](https://geocode.earth/).

Like satellite imagery, it's probably not practical to host a planetwide geocoding dataset unless you're selling a service on top of it, (but don't let me stop you from trying).

## Legends and other bespoke controls

Finally, there's all the stuff that goes with and around and on top of maps: Legends, controls and other UI elements. Some of these come bundled with Maplibre or whatever rendering engine you have. Some, you will have to build yourself.

My [wildfires map](https://muckrock.github.io/wildfires-protomaps/#4/39.28/-101.57) is wrapped in a set of [Svelte](https://svelte.dev/) components to manage interactivity. I built a small [legend component](https://github.com/MuckRock/wildfires-protomaps/blob/main/src/Legend.svelte) and used Svelte's [templating](https://github.com/MuckRock/wildfires-protomaps/blob/main/src/App.svelte#L138-L163) and [reactivity](https://github.com/MuckRock/wildfires-protomaps/blob/main/src/App.svelte#L30) to handle layer switching.

This is the sort of thing that is probably going to be a little different in every project. That `Legend.svelte` file is probably too small to be worth packaging -- I'll just copy it into the next map I make.

Like the rest of the self-hosted map stack, there are solutions to all of these problems, even if they're all packaged and maintained separately. Some are barely documented or out of date. Some are in Java.

It's an ecosystem, and it's going to take some exploration.
