import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def get_latest_news() -> list:
    """Fetches recent financial news via Google News RSS for Indian Business."""
    url = "https://news.google.com/rss/search?q=India+Business+Finance&hl=en-IN&gl=IN&ceid=IN:en"
    news_items = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('./channel/item')[:10]: # Top 10
                title = item.find('title').text if item.find('title') is not None else ""
                link = item.find('link').text if item.find('link') is not None else ""
                pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ""
                news_items.append({"title": title, "link": link, "date": pubDate, "summary": "AI Summary placeholder."})
    except Exception as e:
        pass
    return news_items
