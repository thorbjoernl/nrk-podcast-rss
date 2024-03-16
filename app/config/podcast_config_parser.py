from __future__ import annotations
from typing import Optional, Mapping
import json

DEFAULT_PODCAST_IMAGE_URL = (
    "https://f003.backblazeb2.com/file/VTZ2U-PUBLIC/default_podcast.png"
)
DEFAULT_PODCAST_TITLE = "Untitled Podcast"
DEFAULT_PODCAST_DESC = ""
DEFAULT_PODCAST_EXPLICIT = False


class PodcastConfigurationError(ValueError):
    pass


class PodcastConfigParser:
    """
    Parser for the podcast.json configuration format.

    """

    @staticmethod
    def canonicalize_weekdays(weekdays: Optional[list]) -> set:
        """
        Returns a set of weekdays as a list of numbers, 0-6, where
        0 is monday and 6 is sunday.
        """
        if weekdays is None:
            return set(range(7))

        for i in weekdays:
            if not isinstance(i, int):
                raise PodcastConfigurationError(f"{i} is not an integer.")
            if i < 0 or i >= 7:
                raise PodcastConfigurationError(
                    f"{i} is out of bounds for weekday configuration."
                )

        # TODO: Allow other forms such as ["mon", "tue", ...]
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
        where appropriate and raisin PodcastConfigurationError for required
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

            if not p["url"]:
                raise PodcastConfigurationError(f"Missing url for podcast {i}.")

            if not p["fname"]:
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

            output.append(new_item)

        return output
