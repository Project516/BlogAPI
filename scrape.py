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

        title = heading.get_text(strip=True) if heading else ""
        href = anchor.get("href", "") if anchor else ""
        date = time.get("datetime", "") if time else ""

        # A blog post needs at least a title, a link, and a date. Skip any
        # <article> that is missing one of these instead of letting a single
        # malformed entry abort the whole scrape.
        if not title or not href or not date:
            continue

        blogs.append(
            {
                "title": title,
                "link": urljoin(BLOG_BASE_URL, href),
                "date": date,
            }
        )

    return blogs
