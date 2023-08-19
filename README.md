# NRK podcasts as rss

The purpose of this project is to generate rss feeds for NRK's podcasts which
were recently made exclusive to the NRK radio app. This program uses yt-dlp to
extract meta-data and mp3 urls from radio.nrk.no and generates an rss feed for
the show.

The easiest way to run this program is via the docker-compose file:

- `docker-compose up`

This will start the application, and make the rss feeds available on
http://localhost:800/\*.rss
