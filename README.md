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

## Configuration

The program is configured using the files `config.ini` and `config.json`.

Config.ini has the following options:

[logging]

**level** - The Python [logging level](https://docs.python.org/3/library/logging.html#logging-levels)
used by the program.

[updates]

**frequency** - The interval between refreshing podcasts in seconds.

[podcasts]

**ep_count** - The number of episodes to include when generating the feed.

Config.json is a json file with a list of podcasts to generate for.

```
[
    {
        "name": "Debatten",
        "url": "https://radio.nrk.no/podkast/debatten",
        "desc": "Debatten",
        "image": "https://gfx.nrk.no/Af9YzwX723rS69Qgz3oHLw2IHEwG0DBRpFXyskY8gwrA",
        "fname": "debatten"
    },
    {
        ...
    }
]
```

The following options are available:

- **url** (string; **required**) - The url of the podcast on https://radio.nrk.no
- **fname** (string; **required**) - Root of the filename to be used for the resulting feed. Should be unique between podcasts, and only use characters that are allowed in a file name.
- **name** (string; default: 'Untitled Podcast') - The name of the podcast.
- **desc** (string; default: '') - Description for the podcast.
- **image** (string; default: 'https://raw.githubusercontent.com/thorbjoernl/nrk-podcast-rss/main/img/default_podcast.png') - Image url for the podcast.
- **explicit** (string; default: false) - Boolean indicating whether the podcast contains explicit content.
- **weekdays** (list of integers or strings; default: [0..6]) - If integer 0 is monday and 6 is sunday. If string, the first three characters must match the english name of the weekday. The podcast will only be updated on matching weekdays. Example configurations: ["mon", "tue", "wed", "thu", "fri"], [0, 1, 2, 3, 4]
- **hours** (list of integers; default: [0..23]) - Hours during the days where the podcast will be updated. For example if [7, 8, 9], the podcast will only be updated if current time is 07:XX, 08:XX, 09:XX.
- **episode_count** (int; default: 10) - The number of most recent episodes to fetch for this podcast.

Both weekdays and hours filtering must be met for the podcast to update.
