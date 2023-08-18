import os
import logging
import json
import configparser
import time
import yt_dlp
import datetime
import pytz
import contextlib
from glob import glob
from podgen import Podcast, Episode, Media

OUTPUT_DIR = "/data"
if __name__ == "__main__":
    while True:
        # help(yt_dlp.YoutubeDL)
        config = configparser.ConfigParser()
        config.read("./config/config.ini")

        # Configure logging.
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(config["logging"]["level"])

        u = "https://radio.nrk.no/podkast/dagsnytt_atten"

        ydl = yt_dlp.YoutubeDL({"paths": {"home": OUTPUT_DIR}})
        info = ydl.extract_info(u, download=False, process=False)

        with open("archive.txt") as f:
            archive = f.read().splitlines()

        print(archive)

        pod = Podcast()
        pod.name = "Dagsnytt 18"
        pod.website = "https://radio.nrk.no/serie/dagsnytt-atten"
        pod.description = "Dagsnytt18"
        pod.explicit = False

        for e in info["entries"]:
            if "id" in e.keys():
                if not (e["url"] in archive):
                    episode_info = ydl.extract_info(
                        e["url"], download=False, process=True
                    )

                    ep = Episode()
                    ep.title = episode_info["title"]
                    ep.summary = episode_info.get("summary", "")
                    ep.media = Media(episode_info["url"])
                    ep.publication_date = datetime.datetime.fromtimestamp(
                        episode_info["timestamp"],
                        tz=pytz.timezone("Europe/Oslo"),
                    )
                    pod.add_episode(ep)

                    print(os.path.join(OUTPUT_DIR, "dagsnytt18.rss"))
                    pod.rss_file(os.path.join(OUTPUT_DIR, "dagsnytt18.rss"))

                    with open("archive.txt", "a") as f:
                        f.write(e["url"] + "\n")

        time.sleep(60 * 5)
