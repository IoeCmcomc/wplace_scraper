# wplacescrape

A quickly improvised script to scrape pixel art tiles from wplace.live (think r/place but it's on a world map)

## Usage

No arguments implemented. Just install aiohttp and run ``python3 wplacescrape.py``.

Tiles will be saved relative to the current working directory as files/s0/tiles/[x]/[y]/[timestamp]\.png, where x and y are the coordinates of the map tile and timestamp is the UNIX timestamp (seconds since 1 Jan 1970) when that tile on the map was last modified. The entire map will be downloaded (this should take ~15.7 hours). Requests will be rate-limited to 5 per second to avoid melting their server.

## Technical notes

Underlying world map is MapLibre/Mapbox tiles (this code doesn't save those, it should be easy to get them somewhere else). Pixels get streamed in from urls like https://backend.wplace.live/files/s0/tiles/[x]/[y].png, where x is an integer 0-2047 based on longitude and y is an integer 0-137 based on latitude. (No idea what "s0" means; "season zero"? Are they going to reset the map at some point and increment it?) Each png is 1000x1000 pixels, giving a total canvas size of 2048000x138000 and 282624 tiles in total. The pngs are served from a regular nginx server behind Cloudflare, no attempt is made to authenticate requests (they don't block curl user-agents either). They've probably set Cloudflare to a low blocking setting because the requests are all initiated by XHR through a service worker so there'd be no opportunity for a legitimate (i.e. browser) user to solve a captcha if Cloudflare served one.

The default setting is to make 5 requests by second (by limiting the number of active workers to 5 and making each one sleep 1 second after a successful request), meaning it should take approximately 282,624/5  = 56,524.8 seconds (around 15.7 hours) to download the entire map. (If you try to make more than 5 requests per second, Cloudflare will rate limit you.)

## TODOs

- A way to view the map offline (could just copy wplace.live and point it at the local archive, or do something fancier)
- A way to specify specific areas to scrape rather than the entire map (e.g. only continents as opposed to ocean, only major cities, etc.)

## License

Copyright 2025 Benjamin Lowry

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.