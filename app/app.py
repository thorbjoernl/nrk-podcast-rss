import configparser
import logging
import os
import time

from config.podcast_config_parser import PodcastConfigParser
from const import CONFIG_DIR
from rssextractor import RSSExtractor

config = configparser.ConfigParser()
config.read(os.path.join(CONFIG_DIR, "config.ini"))


def main():
    logging.basicConfig(level=config["logging"]["level"])

    with open(os.path.join(CONFIG_DIR, "config.json"), "r") as f:
        podcasts = PodcastConfigParser.parse_podcasts(f)

    while True:
        refresh_start = time.perf_counter()
        threads: list[RSSExtractor] = []
        for item in podcasts:
            t = RSSExtractor(item)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        refresh_duration = time.perf_counter() - refresh_start

        sleep_duration = max(
            [int(config["updates"]["frequency_sec"]) - refresh_duration, 0]
        )
        logging.info(
            f"Refresh finished in {refresh_duration:.3f} seconds. Next refresh in {sleep_duration:.3f} seconds."
        )
        time.sleep(sleep_duration)


if __name__ == "__main__":
    main()
