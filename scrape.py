import requests
from bs4 import BeautifulSoup


def scrape_blogs(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    blogs = []
    for article in soup.find_all("article"):
        title = article.find("h2").get_text(strip=True)
        link = article.find("a")["href"]
        summary = article.find("p").get_text(strip=True)
        date = article.find("time")["datetime"]
        blogs.append({"title": title, "link": link, "summary": summary, "date": date})

    return blogs
