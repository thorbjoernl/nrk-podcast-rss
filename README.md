# NRK podcasts as rss

The purpose of this project is to generate rss feeds for [NRK's](https://nrk.no)
podcasts which were recently made exclusive to the NRK radio app. This program
<<<<<<< HEAD
uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to extract meta-data and mp3
urls from https://radio.nrk.no and generates an rss feed for the podcast, which
can then be subscribed to by any rss based podcast app.
=======
uses yt-dlp to extract meta-data and mp3 urls from radio.nrk.no and generates an
rss feed for the podcast, which can then be subscribed to by any rss based
podcast app.
>>>>>>> e7fe91c (Use threading, and skip update based on time.)

The easiest way to run this program is via the docker-compose file:

- `docker-compose build`
- `docker-compose up`

This will start the application, and host the rss feeds on
`http://localhost:8000/*.rss`
<<<<<<< HEAD

The first time the program runs it will take a long time to extract the meta-data
from the backlog. Once this is done, updating the feeds is quick, and will likely
take less than 30s per podcast.

Note that once generated the links to mp3s are not kept up to date, and may break
if NRK changes where the episodes are stored on their servers.
=======
>>>>>>> e7fe91c (Use threading, and skip update based on time.)
