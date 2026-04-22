import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from scrape import scrape_blogs
from fastapi import FastAPI, HTTPException, Request
import json
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
@limiter.limit("1/hour")
def get_blogs(request: Request):
    return cache


@app.get("/blogs/latest")
@limiter.limit("1/day")
def get_latest_blogs(request: Request):
    return cache[0] if cache else None


@app.get("/blogs/search")
@limiter.limit("5/hour")
def search_blogs(request: Request, query: str):
    results = []
    for blog in cache:
        if query.lower() in blog["title"].lower():
            results.append(blog)
    return results if results else {"message": "Blog not found"}


@app.post("/blogs/cache")
@limiter.limit("1/week")
def cache_blogs(request: Request):
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
