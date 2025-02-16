import logging
from unittest.mock import MagicMock, patch

import pytest
import requests

from doteki.plugins.feed import run, validate_settings

MOCK_YOUTUBE_FEED_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns:media="http://search.yahoo.com/mrss/" xmlns="http://www.w3.org/2005/Atom">
 <link rel="self" href="http://www.youtube.com/feeds/videos.xml?channel_id=UCSample12345"/>
 <id>yt:channel:UCSample12345</id>
 <yt:channelId>UCSample12345</yt:channelId>
 <title>test channel</title>
 <link rel="alternate" href="https://www.youtube.com/channel/UCSample12345"/>
 <author>
  <name>test channel</name>
  <uri>https://www.youtube.com/channel/UCSample12345</uri>
 </author>
 <published>2023-01-01T00:00:00+00:00</published>

 <entry>
  <id>yt:video:Video1</id>
  <yt:videoId>Video1</yt:videoId>
  <yt:channelId>UCSample12345</yt:channelId>
  <title>Video1</title>
  <link rel="alternate" href="https://www.youtube.com/watch?v=Video1"/>
  <author>
   <name>test channel</name>
   <uri>https://www.youtube.com/channel/UCSample12345</uri>
  </author>
  <published>2023-01-01T10:00:00+00:00</published>
  <updated>2023-01-02T10:00:00+00:00</updated>
  <media:group>
   <media:title>Video1</media:title>
   <media:content url="https://www.youtube.com/v/Video1?version=3" type="application/x-shockwave-flash" width="640" height="390"/>
   <media:thumbnail url="https://i1.ytimg.com/vi/Video1/hqdefault.jpg" width="480" height="360"/>
   <media:description>Description of Video1.</media:description>
   <media:community>
    <media:starRating count="10" average="4.5" min="1" max="5"/>
    <media:statistics views="1000"/>
   </media:community>
  </media:group>
 </entry>

 <entry>
  <id>yt:video:Video2</id>
  <yt:videoId>Video2</yt:videoId>
  <yt:channelId>UCSample12345</yt:channelId>
  <title>Video2</title>
  <link rel="alternate" href="https://www.youtube.com/watch?v=Video2"/>
  <author>
   <name>test channel</name>
   <uri>https://www.youtube.com/channel/UCSample12345</uri>
  </author>
  <published>2023-02-01T08:30:00+00:00</published>
  <updated>2023-02-02T09:30:00+00:00</updated>
  <media:group>
   <media:title>Video2</media:title>
   <media:content url="https://www.youtube.com/v/Video2?version=3" type="application/x-shockwave-flash" width="640" height="390"/>
   <media:thumbnail url="https://i1.ytimg.com/vi/Video2/hqdefault.jpg" width="480" height="360"/>
   <media:description>Description of Video2.</media:description>
   <media:community>
    <media:starRating count="15" average="4.7" min="1" max="5"/>
    <media:statistics views="500"/>
   </media:community>
  </media:group>
 </entry>

 <entry>
  <id>yt:video:Video3</id>
  <yt:videoId>Video3</yt:videoId>
  <yt:channelId>UCSample12345</yt:channelId>
  <title>Video3</title>
  <link rel="alternate" href="https://www.youtube.com/watch?v=Video3"/>
  <author>
   <name>test channel</name>
   <uri>https://www.youtube.com/channel/UCSample12345</uri>
  </author>
  <published>2023-03-15T11:20:00+00:00</published>
  <updated>2023-03-16T12:20:00+00:00</updated>
  <media:group>
   <media:title>Video3</media:title>
   <media:content url="https://www.youtube.com/v/Video3?version=3" type="application/x-shockwave-flash" width="640" height="390"/>
   <media:thumbnail url="https://i1.ytimg.com/vi/Video3/hqdefault.jpg" width="480" height="360"/>
   <media:description>Description of Video3.</media:description>
   <media:community>
    <media:starRating count="20" average="4.8" min="1" max="5"/>
    <media:statistics views="2000"/>
   </media:community>
  </media:group>
 </entry>
</feed>
"""

MOCK_ATOM_FEED_XML = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>Example Tech Blog</title>
    <subtitle>Exploring Technology and Programming</subtitle>
    <link href="https://example.com/atom.xml" rel="self" type="application/atom+xml"/>
    <link href="https://example.com"/>
    <updated>2023-12-16T00:00:00+00:00</updated>
    <id>https://example.com/atom.xml</id>

    <entry>
        <title>Understanding Machine Learning Algorithms</title>
        <published>2023-12-15T08:30:00+00:00</published>
        <updated>2023-12-15T09:00:00+00:00</updated>
        <author>
            <name>Jane Doe</name>
        </author>
        <link rel="alternate" href="https://example.com/machine-learning-algorithms" type="text/html"/>
        <id>https://example.com/machine-learning-algorithms</id>
        <summary type="html">A deep dive into various machine learning algorithms and their real-world applications.</summary>
    </entry>

    <entry>
        <title>Breaking Down Cryptography Basics</title>
        <published>2023-12-10T11:00:00+00:00</published>
        <updated>2023-12-10T11:30:00+00:00</updated>
        <author>
            <name>John Smith</name>
        </author>
        <link rel="alternate" href="https://example.com/cryptography-basics" type="text/html"/>
        <id>https://example.com/cryptography-basics</id>
        <summary type="html">An introduction to cryptography, exploring its history and fundamental concepts.</summary>
    </entry>

    <entry>
        <title>Exploring the Future of Quantum Computing</title>
        <published>2023-11-30T14:45:00+00:00</published>
        <updated>2023-11-30T15:00:00+00:00</updated>
        <author>
            <name>Alice Johnson</name>
        </author>
        <link rel="alternate" href="https://example.com/quantum-computing-future" type="text/html"/>
        <id>https://example.com/quantum-computing-future</id>
        <summary type="html">A speculative look at how quantum computing could evolve and impact various industries.</summary>
    </entry>

    <entry>
        <title>Artificial Intelligence Ethics: A Modern Discussion</title>
        <published>2023-11-10T12:30:00+00:00</published>
        <updated>2023-11-10T13:00:00+00:00</updated>
        <author>
            <name>Michael Brown</name>
        </author>
        <link rel="alternate" href="https://example.com/ai-ethics" type="text/html"/>
        <id>https://example.com/ai-ethics</id>
        <summary type="html">Exploring the ethical implications and challenges of artificial intelligence in today's world.</summary>
    </entry>
</feed>
"""


@patch("requests.get")
def test_youtube_feed(mock_get):
    # Create a mock response object.
    mock_response = MagicMock()
    mock_response.content = MOCK_YOUTUBE_FEED_XML
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id=123",
        "n": 2,
    }
    result = run(settings)

    expected_output = [
        "[Video1](https://www.youtube.com/watch?v=Video1)",
        "[Video2](https://www.youtube.com/watch?v=Video2)",
    ]

    assert result == expected_output
    mock_get.assert_called_with(
        "https://www.youtube.com/feeds/videos.xml?channel_id=123"
    )


@patch("requests.get")
def test_atom_feed(mock_get):
    # Create a mock response.
    mock_response = MagicMock()
    mock_response.content = MOCK_ATOM_FEED_XML
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {
        "url": "https://example.com/atom.xml",
        "n": 3,
    }
    result = run(settings)

    expected_output = [
        "[Understanding Machine Learning Algorithms](https://example.com/machine-learning-algorithms)",
        "[Breaking Down Cryptography Basics](https://example.com/cryptography-basics)",
        "[Exploring the Future of Quantum Computing](https://example.com/quantum-computing-future)",
    ]
    assert result == expected_output
    mock_get.assert_called_with("https://example.com/atom.xml")


def test_missing_url(caplog):
    settings = {}
    with caplog.at_level(logging.ERROR):
        result = run(settings)
    assert result is None
    assert "No url provided for the Feed plugin" in caplog.text


def test_invalid_url(caplog):
    settings = {"url": "http:/invalid/.url"}
    with caplog.at_level(logging.ERROR):
        result = run(settings)
    assert result is None
    assert "Error fetching the feed" in caplog.text


def test_empty_response(caplog):
    mock_response = MagicMock()
    mock_response.content = ""
    mock_response.raise_for_status = MagicMock()
    with patch("requests.get", return_value=mock_response):
        settings = {"url": "https://example.com/atom.xml"}
        with caplog.at_level(logging.ERROR):
            result = run(settings)
        assert result is None
        assert "The response from the URL is empty" in caplog.text


def test_malformed_feed(caplog):
    mock_response = MagicMock()
    mock_response.content = b"Not a valid feed content"
    mock_response.raise_for_status = MagicMock()
    with patch("requests.get", return_value=mock_response):
        settings = {"url": "https://example.com/atom.xml"}
        with caplog.at_level(logging.ERROR):
            result = run(settings)
        assert result is None
        assert "Malformed feed: no entries found" in caplog.text


@patch("requests.get")
@patch("feedparser.parse")
def test_error_processing_feed(mock_parse, mock_get, caplog):
    # Configure mock_parse to raise an exception.
    mock_parse.side_effect = Exception("Parsing error")
    mock_response = MagicMock()
    mock_response.content = b"Some feed content"
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {
        "url": "https://example.com/atom.xml",
    }

    with caplog.at_level(logging.ERROR):
        result = run(settings)

    assert result is None
    assert "Error processing the feed" in caplog.text


@pytest.mark.parametrize(
    "exception",
    [
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.HTTPError,
    ],
)
@patch("requests.get")
def test_request_exceptions(mock_get, caplog, exception):
    mock_get.side_effect = exception
    settings = {"url": "https://example.com/atom.xml"}

    with caplog.at_level(logging.ERROR):
        result = run(settings)

    assert result is None
    assert "Error fetching the feed" in caplog.text


MOCK_FEED_WITH_MISSING_DATA = b"""
<feed>
    <entry>
        <title>Entry 1</title>
        <link href="http://example.com/entry1" />
        <published>2024-01-01T00:00:00Z</published>
    </entry>
    <entry>
        <link href="http://example.com/entry2" />
        <published>2024-01-02T00:00:00Z</published>
    </entry>
</feed>
"""


@patch("requests.get")
def test_feed_with_missing_data(mock_get, caplog):
    # Mock response with the feed having an entry missing a title
    mock_response = MagicMock()
    mock_response.content = MOCK_FEED_WITH_MISSING_DATA
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {"url": "https://example.com/atom.xml", "show_date": True}
    result = run(settings)

    expected_output = [
        "[Entry 1](http://example.com/entry1) · 2024-01-01",
        "[No Title](http://example.com/entry2) · 2024-01-02",
    ]
    assert result == expected_output
    assert "Error" not in caplog.text


def test_invalid_setting_type(caplog):
    settings = {
        "url": 123,
    }
    with caplog.at_level(logging.ERROR):
        result = run(settings)

    assert result is None
    assert "Invalid type for url" in caplog.text


def test_log_multiple_errors(caplog):
    settings = {"url": 123, "n": "3", "show_date": "false"}
    with caplog.at_level(logging.ERROR):
        result = validate_settings(settings)

    assert not result
    assert "Invalid type for url: 'int'. Expected str" in caplog.text
    assert "Invalid type for n: 'str'. Expected int" in caplog.text
    assert "Invalid type for show_date: 'str'. Expected bool" in caplog.text


MOCK_FEED_MISSING_DATE = b"""
<feed>
    <entry>
        <title>Entry w/ date</title>
        <link href="http://example.com/entry1" />
        <published>2024-01-01T00:00:00Z</published>
    </entry>
    <entry>
        <title>Entry w/o date</title>
        <link href="http://example.com/entry2" />
    </entry>
</feed>
"""


@patch("requests.get")
def test_feed_missing_date(mock_get, caplog):
    mock_response = MagicMock()
    mock_response.content = MOCK_FEED_MISSING_DATE
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {"url": "https://example.com/atom.xml", "show_date": True}
    with caplog.at_level(logging.WARNING):
        result = run(settings)

    assert result is not None  # A missing date should not stop the plugin.
    assert "Entry missing date" in caplog.text
    expected_output = [
        "[Entry w/ date](http://example.com/entry1) · 2024-01-01",
        "[Entry w/o date](http://example.com/entry2)",
    ]
    assert result == expected_output


@patch("requests.get")
def test_n_one_returns_str(mock_get):
    mock_response = MagicMock()
    mock_response.content = MOCK_FEED_MISSING_DATE
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {"url": "https://example.com/atom.xml", "n": 1}
    result = run(settings)

    expected_output = "[Entry w/ date](http://example.com/entry1)"
    assert result == expected_output
    assert isinstance(result, str)


@patch("requests.get")
def test_sort_by_published_date(mock_get):
    mock_response = MagicMock()
    mock_response.content = MOCK_ATOM_FEED_XML
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    # Test ascending order
    settings = {
        "url": "https://example.com/atom.xml",
        "sort_order": "ascending",
        "sort_field": "published",
    }
    result = run(settings)
    assert result[0].startswith("[Artificial Intelligence Ethics")  # Oldest
    assert result[-1].startswith("[Understanding Machine Learning")  # Newest

    # Test descending order
    settings["sort_order"] = "descending"
    result = run(settings)
    assert result[0].startswith("[Understanding Machine Learning")  # Newest
    assert result[-1].startswith("[Artificial Intelligence Ethics")  # Oldest


@patch("requests.get")
def test_sort_by_updated_date(mock_get):
    mock_response = MagicMock()
    mock_response.content = MOCK_ATOM_FEED_XML
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {
        "url": "https://example.com/atom.xml",
        "sort_order": "descending",
        "sort_field": "updated",
    }
    result = run(settings)
    assert result[0].startswith("[Understanding Machine Learning")  # Last updated
    assert result[-1].startswith("[Artificial Intelligence Ethics")  # First updated


MOCK_FEED_MIXED_DATES = b"""
<feed>
    <entry>
        <title>Entry 1</title>
        <link href="http://example.com/entry1" />
        <published>2024-01-01T00:00:00Z</published>
        <updated>2024-01-02T00:00:00Z</updated>
    </entry>
    <entry>
        <title>Entry 2</title>
        <link href="http://example.com/entry2" />
        <published>2024-01-02T00:00:00Z</published>
    </entry>
    <entry>
        <title>Entry 3</title>
        <link href="http://example.com/entry3" />
        <published>2024-01-03T00:00:00Z</published>
        <updated>2024-01-01T00:00:00Z</updated>
    </entry>
</feed>
"""


@pytest.mark.filterwarnings(
    "ignore:To avoid breaking existing software:DeprecationWarning"
)
@patch("requests.get")
def test_sort_with_mixed_dates(mock_get):
    mock_response = MagicMock()
    mock_response.content = MOCK_FEED_MIXED_DATES
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    # Test sorting by updated - the order should be:
    # Entry 3 (Jan 1), Entry 1 (Jan 2), Entry 2 (falls back to published date Jan 2)
    settings = {
        "url": "https://example.com/atom.xml",
        "sort_order": "ascending",
        "sort_field": "updated",
    }
    result = run(settings)

    assert len(result) == 3
    assert result[0].startswith("[Entry 3")  # Updated Jan 1
    assert result[1].startswith("[Entry 1")  # Updated Jan 2
    # Entry 2 should be last, using its published date as fallback
    assert result[2].startswith("[Entry 2")


def test_invalid_sort_parameters(caplog):
    settings = {
        "url": "https://example.com/atom.xml",
        "sort_order": "invalid",
        "sort_field": "published",
    }
    with caplog.at_level(logging.ERROR):
        result = run(settings)
    assert result is None
    assert "Invalid sort_order: 'invalid'" in caplog.text

    settings = {
        "url": "https://example.com/atom.xml",
        "sort_order": "ascending",
        "sort_field": "invalid",
    }
    with caplog.at_level(logging.ERROR):
        result = run(settings)
    assert result is None
    assert "Invalid sort_field: 'invalid'" in caplog.text


MOCK_FEED_UPDATED_FALLBACK = b"""
<feed>
    <entry>
        <title>Entry 1</title>
        <link href="http://example.com/entry1" />
        <published>2024-01-01T00:00:00Z</published>
        <updated>2024-01-03T00:00:00Z</updated>
    </entry>
    <entry>
        <title>Entry 2</title>
        <link href="http://example.com/entry2" />
        <published>2024-01-02T00:00:00Z</published>
    </entry>
    <entry>
        <title>Entry 3</title>
        <link href="http://example.com/entry3" />
        <published>2024-01-03T00:00:00Z</published>
        <updated>2024-01-01T00:00:00Z</updated>
    </entry>
</feed>
"""


@pytest.mark.filterwarnings(
    "ignore:To avoid breaking existing software:DeprecationWarning"
)
@patch("requests.get")
def test_sort_updated_fallback(mock_get):
    mock_response = MagicMock()
    mock_response.content = MOCK_FEED_UPDATED_FALLBACK
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    settings = {
        "url": "https://example.com/atom.xml",
        "sort_order": "ascending",
        "sort_field": "updated",
    }
    result = run(settings)

    # In ascending order:
    # Entry 3 (updated Jan 1)
    # Entry 2 (no updated, published Jan 2)
    # Entry 1 (updated Jan 3)
    assert len(result) == 3
    assert result[0].startswith("[Entry 3")  # Updated earliest
    assert result[1].startswith("[Entry 2")  # Uses published date as fallback
    assert result[2].startswith("[Entry 1")  # Updated latest

    # Test descending order too
    settings["sort_order"] = "descending"
    result = run(settings)
    assert result[0].startswith("[Entry 1")  # Updated latest
    assert result[1].startswith("[Entry 2")  # Uses published date as fallback
    assert result[2].startswith("[Entry 3")  # Updated earliest


MOCK_FEED_NO_DATES = b"""
<feed>
    <entry>
        <title>Entry 1</title>
        <link href="http://example.com/entry1" />
        <published>2024-01-01T00:00:00Z</published>
    </entry>
    <entry>
        <title>Entry 2</title>
        <link href="http://example.com/entry2" />
    </entry>
    <entry>
        <title>Entry 3</title>
        <link href="http://example.com/entry3" />
        <published>2024-01-03T00:00:00Z</published>
    </entry>
</feed>
"""


@patch("requests.get")
def test_sort_with_missing_all_dates(mock_get, caplog):
    mock_response = MagicMock()
    mock_response.content = MOCK_FEED_NO_DATES
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    # Test ascending order - dateless entries should be at the end.
    settings = {
        "url": "https://example.com/atom.xml",
        "sort_order": "ascending",
        "sort_field": "published",
    }
    result = run(settings)

    assert len(result) == 3
    assert result[0].startswith("[Entry 1")  # Jan 1
    assert result[1].startswith("[Entry 3")  # Jan 3
    assert result[2].startswith("[Entry 2")  # No date -> should be last in ascending

    # Test descending order - dateless entries should still be at the end.
    settings["sort_order"] = "descending"
    result = run(settings)
    assert result[0].startswith("[Entry 3")  # Jan 3
    assert result[1].startswith("[Entry 1")  # Jan 1
    assert result[2].startswith("[Entry 2")  # No date -> should be last in descending
