from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}


@app.get("/double")
def double(x: int):
    return {"result": x * 2}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

uvicorn.run(app)
