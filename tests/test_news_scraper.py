import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from news_scraper import get_latest_news

def test_get_latest_news():
    news = get_latest_news()
    assert isinstance(news, list)
    # Even if empty, it should be a list. If not empty, check dictionary keys
    if news:
        assert "title" in news[0]
        assert "link" in news[0]
