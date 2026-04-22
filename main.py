from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from scrape import scrape_blogs
import json

app = FastAPI()

try:
    with open("cache.json", "r") as file:
        cache = json.load(file)
except FileNotFoundError:
    cache = []

latest = cache[0] if cache else None


@app.get("/blogs")
def get_blogs():
    return cache


@app.get("/blogs/latest")
def get_latest_blogs():
    return latest


@app.get("/blogs/search")
def search_blogs(query: str):
    results = []
    for blog in cache:
        if query.lower() in blog["title"].lower():
            results.append(blog)
    return results if results else {"message": "Blog not found"}


@app.post("/blogs/cache")
def cache_blogs():
    cache = scrape_blogs(
        "https://raw.githubusercontent.com/Project516/project516.github.io/refs/heads/master/blog.html"
    )
    with open("cache.json", "w") as file:
        json.dump(cache, file)
    return {"message": "Blogs cached successfully"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

uvicorn.run(app)
