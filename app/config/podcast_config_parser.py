from __future__ import annotations

import json
from typing import Mapping, Optional

DEFAULT_PODCAST_IMAGE_URL = "https://raw.githubusercontent.com/thorbjoernl/nrk-podcast-rss/main/img/default_podcast.png"
DEFAULT_PODCAST_TITLE = "Untitled Podcast"
DEFAULT_PODCAST_DESC = ""
DEFAULT_PODCAST_EXPLICIT = False
DEFAULT_PODCAST_EPISODE_COUNT = 10

WEEKDAY_PREFIXES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


class PodcastConfigurationError(ValueError):
    pass


class PodcastConfigParser:
    """
    Parser for the podcast.json configuration format.

    """

    @staticmethod
    def weekdaystr_as_int(weekday: str | int) -> int:
        """ """
        if isinstance(weekday, int):
            return weekday

        for i, s in enumerate(WEEKDAY_PREFIXES):
            if s == weekday.lower()[0:3]:
                return i

        raise PodcastConfigurationError(
            "Could not convert weekday, {weekday} to integer."
        )

    @staticmethod
    def canonicalize_weekdays(weekdays: Optional[list]) -> set:
        """
        Returns a set of weekdays as a set of numbers, 0-6, where
        0 is monday and 6 is sunday.
        """
        if weekdays is None:
            return set(range(7))

        weekdays = list(
            map(lambda x: PodcastConfigParser.weekdaystr_as_int(x), weekdays)
        )

        for i in weekdays:
            if not isinstance(i, int):
                raise PodcastConfigurationError(f"{i} is not an integer.")
            if i < 0 or i >= 7:
                raise PodcastConfigurationError(
                    f"{i} is out of bounds for weekday configuration."
                )

        return set(weekdays)

    @staticmethod
    def canonicalize_hours(hours: Optional[list]) -> set:
        """
        Returns the set of hours as a set of integers between 0 and 23. Defaults
        to all hours if hours is None.
        """
        if hours is None:
            return set(range(24))

        for i in hours:
            if not isinstance(i, int):
                raise PodcastConfigurationError(f"{i} is not an integer.")
            if i < 0 or i >= 24:
                raise PodcastConfigurationError(
                    f"{i} is out of bounds for hours configuration."
                )
        return set(hours)

    @staticmethod
    def parse_podcasts(f) -> list[dict]:
        """
        Parses a podcast.json config file, setting missing values to defaults
        where appropriate and raising PodcastConfigurationError for required
        options.
        f can be a file, or a list of mappings.
        Returns a list of dicts.
        """

        output = []

        if not isinstance(f, list):
            f = json.load(f)

        p: Mapping
        for i, p in enumerate(f, start=1):
            new_item = {}

            if not p.get("url", None):
                raise PodcastConfigurationError(f"Missing url for podcast {i}.")

            if not p.get("fname", None):
                raise PodcastConfigurationError(f"Missing fname for podcast {i}.")

            new_item["url"] = p["url"]
            new_item["fname"] = p["fname"]

            new_item["name"] = p.get("name", DEFAULT_PODCAST_TITLE)
            new_item["desc"] = p.get("desc", DEFAULT_PODCAST_DESC)
            new_item["image"] = p.get("image", DEFAULT_PODCAST_IMAGE_URL)
            new_item["explicit"] = p.get("explicit", DEFAULT_PODCAST_EXPLICIT)

            new_item["weekdays"] = PodcastConfigParser.canonicalize_weekdays(
                p.get("weekdays", None)
            )
            new_item["hours"] = PodcastConfigParser.canonicalize_hours(
                p.get("hours", None)
            )

            new_item["episode_count"] = p.get(
                "deepisode_countlay", DEFAULT_PODCAST_EPISODE_COUNT
            )

            output.append(new_item)

        return output
