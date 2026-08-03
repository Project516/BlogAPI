from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BLOG_BASE_URL = "https://project516.dev/"


def scrape_blogs(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, timeout=10, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    blogs = []
    for article in soup.find_all("article"):
        heading = article.find("h3")
        anchor = article.find("a")
        time = article.find("time")

        # A blog post needs at least a title, a link, and a date. Skip any
        # <article> that is missing one of these instead of letting a single
        # malformed entry abort the whole scrape.
        if heading is None or anchor is None or time is None:
            continue

        href = anchor.get("href")
        if href is None:
            continue

        datetime = time.get("datetime")
        if datetime is None:
            continue

        blogs.append(
            {
                "title": heading.get_text(strip=True),
                "link": urljoin(BLOG_BASE_URL, href),
                "date": datetime,
            }
        )

    return blogs
