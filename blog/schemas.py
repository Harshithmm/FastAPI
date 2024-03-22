from typing import List, Optional
from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: list[Blog]  #instead of ShowBlog we can use Blog also bcz 
    class Config():
        orm_mode = True

#moved down bcz we need ShowUser in ShowBlog


class ShowBlog(BaseModel):
    title: str
    body: str
    creator:ShowUser
    class Config():
        orm_mode = True  #if i do this only title will be shown in the response and not the id or body

# class ShowBlog(Blog):
#     class Config():
#         orm_mode = True   
        
class Login(BaseModel):
    username: str
    password: str

#here for below model means schema bcz they are pydantic models and not sqlalchemy models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None