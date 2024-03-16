import pytest
from config.podcast_config_parser import (
    PodcastConfigParser,
    PodcastConfigurationError,
    DEFAULT_PODCAST_IMAGE_URL,
    DEFAULT_PODCAST_DESC,
    DEFAULT_PODCAST_EXPLICIT,
    DEFAULT_PODCAST_TITLE,
)


def test_exceptions():
    # Test exception on missing required options.
    with pytest.raises(PodcastConfigurationError):
        PodcastConfigParser.parse_podcasts([{}])

    with pytest.raises(PodcastConfigurationError):
        PodcastConfigParser.parse_podcasts([{"url": "Test"}])

    # Test exception when wrong type / out of bounds filter settings.
    with pytest.raises(PodcastConfigurationError):
        PodcastConfigParser.parse_podcasts(
            [{"url": "Test", "fname": "Test", "weekdays": [-1]}]
        )

    with pytest.raises(PodcastConfigurationError):
        PodcastConfigParser.parse_podcasts(
            [{"url": "Test", "fname": "Test", "weekdays": [8]}]
        )

    with pytest.raises(PodcastConfigurationError):
        PodcastConfigParser.parse_podcasts(
            [{"url": "Test", "fname": "Test", "weekdays": ["23"]}]
        )

    with pytest.raises(PodcastConfigurationError):
        PodcastConfigParser.parse_podcasts(
            [{"url": "Test", "fname": "Test", "hours": [-1]}]
        )

    with pytest.raises(PodcastConfigurationError):
        PodcastConfigParser.parse_podcasts(
            [{"url": "Test", "fname": "Test", "hours": [25]}]
        )

    with pytest.raises(PodcastConfigurationError):
        PodcastConfigParser.parse_podcasts(
            [{"url": "Test", "fname": "Test", "hours": ["25"]}]
        )


def test_defaults():
    podcasts = PodcastConfigParser.parse_podcasts([{"url": "test", "fname": "test"}])

    assert podcasts[0]["name"] == DEFAULT_PODCAST_TITLE
    assert podcasts[0]["desc"] == DEFAULT_PODCAST_DESC
    assert podcasts[0]["image"] == DEFAULT_PODCAST_IMAGE_URL
    assert podcasts[0]["explicit"] == DEFAULT_PODCAST_EXPLICIT
    assert podcasts[0]["weekdays"] == set(range(7))
    assert podcasts[0]["hours"] == set(range(24))


def test_assignment():
    assert (
        PodcastConfigParser.parse_podcasts(
            [{"url": "test", "fname": "test", "name": "Some name"}]
        )[0]["name"]
        == "Some name"
    )

    assert (
        PodcastConfigParser.parse_podcasts(
            [{"url": "test", "fname": "test", "desc": "Some desc"}]
        )[0]["desc"]
        == "Some desc"
    )

    assert (
        PodcastConfigParser.parse_podcasts(
            [{"url": "test", "fname": "test", "explicit": True}]
        )[0]["explicit"]
        == True
    )

    assert (
        PodcastConfigParser.parse_podcasts(
            [{"url": "test", "fname": "test", "image": "SomeImageURL"}]
        )[0]["image"]
        == "SomeImageURL"
    )


def test_str_weekdays():
    assert PodcastConfigParser.parse_podcasts(
        [{"url": "test", "fname": "test", "weekdays": ["mon", "tue", 4]}]
    )[0]["weekdays"] == set([0, 1, 4])

    assert PodcastConfigParser.parse_podcasts(
        [{"url": "test", "fname": "test", "weekdays": ["monday", "wednesday", 6]}]
    )[0]["weekdays"] == set([0, 2, 6])
