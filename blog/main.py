from fastapi import FastAPI,Depends,status,Response,HTTPException
#status is used to give the status code @app.post('/blog',status_code=status.HTTP_201_CREATED)
#Response is used to give the response in the form of json if not blog:
        # return Response(status_code=status.HTTP_404_NOT_FOUND)
from pydantic import BaseModel
from . import models, schemas
from blog.database import SessionLocal, engine,get_db
from .routers import blog
from .routers import user

app = FastAPI()
models.Base.metadata.create_all(bind=engine) # this will create the table in the database however if already created it will not create again and we can remove this line


app.include_router(blog.router)
app.include_router(user.router)

# class Blog(BaseModel):
#     title: str
#     body: str


# The db.refresh(new_blog) line is used in SQLAlchemy to update the current session with the most recent data for the new_blog object from the database.

# Here's what it does:

# It tells SQLAlchemy to query the database and update the current state of new_blog with any new changes that might have happened in the database.

# This is useful if the database might have been modified by other processes or if the object has database-triggered attributes whose values are only known after you insert, update, or call a database function.

# It ensures that the new_blog object in your current session is up-to-date with the latest data in the database.

# In summary, db.refresh(new_blog) is used to update the new_blog object with the latest data from the database.