import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from news_scraper import get_latest_news

@patch('requests.get')
def test_get_latest_news_mocked(mock_get):
    mock_xml = b"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Market Update</title>
                <link>https://example.com/news1</link>
            </item>
        </channel>
    </rss>"""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.content = mock_xml
    mock_get.return_value = mock_resp
    
    news = get_latest_news()
    assert isinstance(news, list)
    if news:
        assert "title" in news[0]
        assert "link" in news[0]
