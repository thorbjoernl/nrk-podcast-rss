# NRK podcasts as rss

The purpose of this project is to generate rss feeds for [NRK's](https://nrk.no)
podcasts which were recently made exclusive to the NRK radio app. This program
uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to extract meta-data and mp3
urls from https://radio.nrk.no and generates an rss feed for the podcast, which
can then be subscribed to by any rss based podcast app.

The easiest way to run this program is via the docker-compose file:

- `docker-compose build`
- `docker-compose up`

This will start the application, and host the rss feeds on
`http://localhost:8000/*.rss`
