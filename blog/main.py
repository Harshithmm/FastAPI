from fastapi import FastAPI,Depends,status,Response,HTTPException
#status is used to give the status code @app.post('/blog',status_code=status.HTTP_201_CREATED)
#Response is used to give the response in the form of json if not blog:
        # return Response(status_code=status.HTTP_404_NOT_FOUND)
from pydantic import BaseModel
from . import models, schemas
from blog.database import SessionLocal, engine
from sqlalchemy.orm import Session
from .hashing import Hash

models.Base.metadata.create_all(bind=engine) # this will create the table in the database however if already created it will not create again and we can remove this line

app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(blog:schemas.Blog,db : Session=Depends(get_db)):    # this is inside the blog if we execute uviorn main:app --reload this will not be executed hence we need to use uviorn blog.main:app --reload
    new_blog = models.Blog(title=blog.title,body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id,db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Deleted"

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id,request:schemas.Blog, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    
    blog.title = request.title
    blog.body = request.body
    #db.update(blog)
                                #   OR
    # blog.update({'title':blog.title,'body':blog.body},synchronize_session=False)
    db.commit()
    db.refresh(blog)
    return "Updated"

@app.get('/blog',response_model=list[schemas.ShowBlog], tags=['blogs'])
def get_all_blogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',response_model=schemas.ShowBlog, tags=['blogs'])
def get_blog(id,db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
        
    return blog


@app.post('/user',response_model=schemas.ShowUser, tags=['user'])
def create_user(request:schemas.User,db : Session=Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=schemas.ShowUser, tags=['user'])
def get_user(id:int,db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not available")
    return user
# The db.refresh(new_blog) line is used in SQLAlchemy to update the current session with the most recent data for the new_blog object from the database.

# Here's what it does:

# It tells SQLAlchemy to query the database and update the current state of new_blog with any new changes that might have happened in the database.

# This is useful if the database might have been modified by other processes or if the object has database-triggered attributes whose values are only known after you insert, update, or call a database function.

# It ensures that the new_blog object in your current session is up-to-date with the latest data in the database.

# In summary, db.refresh(new_blog) is used to update the new_blog object with the latest data from the database.