from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from scrape import scrape_blogs
import json

app = FastAPI()


@app.get("/blogs")
def get_blogs():
    return scrape_blogs(
        "https://raw.githubusercontent.com/Project516/project516.github.io/refs/heads/master/blog.html"
    )


@app.get("/blogs/latest")
def get_latest_blogs():
    return scrape_blogs(
        "https://raw.githubusercontent.com/Project516/project516.github.io/refs/heads/master/blog.html"
    )


@app.get("/blogs/search")
def search_blogs(query: str):
    return scrape_blogs(
        "https://raw.githubusercontent.com/Project516/project516.github.io/refs/heads/master/blog.html"
    )


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
