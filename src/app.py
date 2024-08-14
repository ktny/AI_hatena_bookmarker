from fastapi import FastAPI
from mangum import Mangum

from libs.bookmark import bookmark

app = FastAPI()


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


@app.post("/bookmark")
async def bookmark_entry(url: str):
    """
    指定URLをブックマークやスター付与を行う
    """
    bookmark(url)


lambda_handler = Mangum(app)
