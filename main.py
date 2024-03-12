from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello, World"}

@app.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    # only get 10 published blogs
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from the db'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]

@app.post('/blog')
def create_blog(blog: Blog):   #for FromBody we need to use Pydantic BaseModel
    return {'data': f'Blog is created with {blog.title} with a {blog.body} and published at {blog.published_at}'}


if __name__ == "__main__":       # if u want to change the port and host
    uvicorn.run(app, host="127.0.0.1", port=9000)  # only works on python main.py not on uvicorn main:app --reload  and for debugging purposes