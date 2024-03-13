from typing import List, Optional
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True  #if i do this only title will be shown in the response and not the id or body

# class ShowBlog(Blog):
#     class Config():
#         orm_mode = True   
        
class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True