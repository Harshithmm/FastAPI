from fastapi import APIRouter, Depends, status, HTTPException

from blog import schemas, database, models
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.get('/blog',response_model=list[schemas.ShowBlog], tags=['blogs'])
def get_all_blogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog',status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(blog:schemas.Blog,db : Session=Depends(get_db)):    # this is inside the blog if we execute uviorn main:app --reload this will not be executed hence we need to use uviorn blog.main:app --reload
    new_blog = models.Blog(title=blog.title,body=blog.body, user_id=2)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id,db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Deleted"

@router.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
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

# @app.get('/blog',response_model=list[schemas.ShowBlog], tags=['blogs'])
# def get_all_blogs(db: Session=Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

@router.get('/blog/{id}',response_model=schemas.ShowBlog, tags=['blogs'])
def get_blog(id,db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
        
    return blog

