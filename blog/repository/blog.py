from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

def get_all(db: Session,current_user):
    blogs = db.query(models.Blog).all()
    return {"data":current_user}

def create_blog(blog,db : Session):
    new_blog = models.Blog(title=blog.title,body=blog.body, user_id=2)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete_blog(id,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Deleted"

def update_blog(id,request, db: Session):
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

def get_blog(id,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
        
    return blog