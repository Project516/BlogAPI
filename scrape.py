import requests
from bs4 import BeautifulSoup


def scrape_blogs(url: str) -> list[dict[str, str]]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, timeout=10, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    blogs = []
    for article in soup.find_all("article"):
        title = article.find("h3").get_text(strip=True)
        link = article.find("a")
        if link is None:
            continue
        link = "https://project516.dev/" + link["href"]
        date = article.find("time")["datetime"]
        blogs.append({"title": title, "link": link, "date": date})

    return blogs
