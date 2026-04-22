from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from scrape import scrape_blogs
from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

try:
    with open("cache.json", "r") as file:
        cache = json.load(file)
except FileNotFoundError:
    cache = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/blogs")
def get_blogs():
    return cache


@app.get("/blogs/latest")
def get_latest_blogs():
    return cache[0] if cache else None


@app.get("/blogs/search")
def search_blogs(query: str):
    results = []
    for blog in cache:
        if query.lower() in blog["title"].lower():
            results.append(blog)
    return results if results else {"message": "Blog not found"}


@app.post("/blogs/cache")
def cache_blogs():
    global cache
    try:
        cache = scrape_blogs(
            "https://raw.githubusercontent.com/Project516/project516.github.io/refs/heads/master/blog.html"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while scraping blogs: {str(e)}",
        )

    with open("cache.json", "w") as file:
        json.dump(cache, file)
    return {"message": "Blogs cached successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
