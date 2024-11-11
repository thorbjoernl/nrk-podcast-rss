import datetime
import logging
import os
import pickle
import urllib
from threading import Thread

import pytz
import yt_dlp
from const import OUTPUT_DIR, PERSISTENT_DIR
from podgen import Episode, Media, Podcast


class RSSExtractor(Thread):
    """
    Class which implements the extraction of a podcast. It is used the same way
    as a Python threads class (https://docs.python.org/3/library/threading.html).
    """

    def __init__(self, config: dict):
        """
        Initializes the extractor given a configuration dictionary.

        config : dict
            A config dictionary as prepared by
            config.podcast_config_parser.PodcastConfigParser
        """
        super(RSSExtractor, self).__init__()
        self.config = config

    def run(self):
        if not (datetime.datetime.today().weekday() in self.config["weekdays"]):
            logging.info(f"Skipping {self.config['name']} due to weekday filtering.")
            return
        if not (datetime.datetime.now().hour in self.config["hours"]):
            logging.info(f"Skipping {self.config['name']} due to hour filtering.")
            return

        # File paths for generated files.
        archive_file = os.path.join(PERSISTENT_DIR, f"{self.config['fname']}.txt")
        pickle_file = os.path.join(PERSISTENT_DIR, f"{self.config['fname']}.pickle")
        rss_file = os.path.join(OUTPUT_DIR, f"{self.config['fname']}.rss")
        ydl = yt_dlp.YoutubeDL()
        info = ydl.extract_info(self.config["url"], download=False, process=False)
        try:
            with open(archive_file, "r") as f:
                archive = set(f.read().splitlines())
        except FileNotFoundError:
            logging.info("No archive file found.")
            archive = set([])
        if os.path.isfile(pickle_file):
            # https://github.com/lkiesow/python-feedgen/issues/72
            # Workaround for podgen not being able to load from existing rss
            # file.
            logging.info("Loading existing Podcast object from pickle file")
            with open(pickle_file, "rb") as f:
                pod = pickle.load(f)
        else:
            logging.info("No existing pickle found. Create new Podcast object")
            pod = Podcast()
            pod.name = self.config["name"]
            pod.website = self.config["url"]
            pod.description = self.config["desc"]
            pod.explicit = self.config["explicit"]
            pod.image = self.config["image"]

        episode_counter = 0
        for e in info["entries"]:
            # The information returned has entries for both "episodes" and
            # "seasons". Only episodes have an "id" key, so we use that to
            # only process the episodes.
            if "id" in e.keys():
                episode_counter = episode_counter + 1
                logging.info(f"Ep counter is at {episode_counter}")
                if e["url"] in archive:
                    logging.info(
                        f"Skipping episode {e['url']}, due to already being in archive."
                    )
                else:
                    try:
                        episode_info = ydl.extract_info(
                            e["url"], download=False, process=True
                        )
                    except yt_dlp.utils.DownloadError as error:
                        logging.error(
                            f"{self.config['name']} - Failed to download {e['id']}"
                        )
                        logging.info(error)
                    else:
                        ep = Episode()
                        ep.title = episode_info["title"]
                        ep.summary = episode_info.get("summary", "")
                        if(not ep.summary):
                           ep.summary = episode_info.get("alt_title", "")
                        ep.media = Media

                        request = urllib.request.Request(
                            episode_info["url"], method="HEAD"
                        )
                        response = urllib.request.urlopen(request)
                        ep.media = Media(
                            episode_info["url"],
                            size=response.headers["Content-Length"],
                        )
                        ep.publication_date = datetime.datetime.fromtimestamp(
                            episode_info["timestamp"],
                            tz=pytz.timezone("Europe/Oslo"),
                        )
                        ep.image = episode_info["thumbnail"]
                        pod.add_episode(ep)
                        pod.rss_file(os.path.join(rss_file), encoding="UTF-8")
                        with open(archive_file, "a") as f:
                            f.write(e["url"] + "\n")
                        with open(pickle_file, "wb") as f:
                            pickle.dump(pod, f)

            if episode_counter >= int(self.config["episode_count"]):
                logging.info("Finishing due to reaching episode count.")
                break
