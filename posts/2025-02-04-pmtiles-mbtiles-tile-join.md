---
title: Turn PMTiles into MBTiles with tile-join
summary: Sometimes I actually want an SQLite file.
---

Modern map stacks use two main formats to store tiles:

- [MBTiles](https://github.com/mapbox/mbtiles-spec), created by [Mapbox](https://www.mapbox.com/), stores tile data in a SQLite database
- [PMTiles](https://docs.protomaps.com/pmtiles/), created by [Protomaps](https://protomaps.com/), uses a single file archive optimized for HTTP byte range requests

PMTiles is my go-to tile storage for [self-hosted maps](https://chrisamico.com/blog/2024-02-13/self-hosted-maps/), since it can live in cheap cloud storage and serve vector tiles without an intermediate server.

However, there are a couple contexts where I still want MBTiles. I can drop an MBTiles file into [QGIS](https://qgis.org/) and preview the data. If I have something else that reads [SQLite](https://sqlite.org/), I can have it also serve MBTiles.

It's that second context that got me figuring out how to turn PMTiles into MBTiles. I'm working on rebuilding my [Datasette GIS stack](https://github.com/eyeseast/spatial-data-cooking-show), which currently uses [Leaflet](https://leafletjs.com/) and image tiles.

The answer, it turns out, was already installed: `tile-join`, part of [Tippecanoe](https://github.com/felt/tippecanoe?tab=readme-ov-file#tile-join), can read MBTiles _or_ PMTiles and also output either format. The examples only refer to MBTiles, but either format works, as input or output.

Leaflet is great, but image tiles are significantly harder to generate than vector tiles, even though it's an older approach. There's just more tooling now. Since I started working on self-hosted maps, I've wanted to move [datasette-geojson-map](https://github.com/eyeseast/datasette-geojson-map). The biggest issue is tiles.

When I'm using PMTiles, I rely heavily on the [free Protomaps daily planet build](https://docs.protomaps.com/basemaps/downloads), and I use `pmtiles extract` to pull down the area I want. But Datasette is already serving data from SQLite (because that's its whole purpose) and it would be nice to just have everything in one place. There's even a [tile server plugin](https://datasette.io/plugins/datasette-tiles), though it currently ownly works with image tiles.

Here's how to get a local tile extract into MBTiles:

```sh
# extract tiles from a Protomaps daily build
pmtiles extract https://build.protomaps.com/20250120.pmtiles public/base.pmtiles --bbox="-121.916742,32.141279,-113.611078,35.642196" --maxzoom 12

# convert to MBTiles
tile-join -o public/base.mbtiles public/base.pmtiles
```

I haven't tested the limit of this approach, but it does work on the area I used in my [minimalist wildfire map](https://chrisamico.com/blog/2025-01-18/fire-map/). Drop that file into QGIS and you should see a street map with default styles.
