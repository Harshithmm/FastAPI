from fastapi import APIRouter, Depends, status, HTTPException

from blog import schemas, database, models
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository import blog
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)

@router.get('',response_model=list[schemas.ShowBlog])
def get_all_blogs(db: Session=Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    return blog.get_all(db,current_user)

@router.post('',status_code=status.HTTP_201_CREATED)
def create_blog(request:schemas.Blog,db : Session=Depends(get_db)):    # this is inside the blog if we execute uviorn main:app --reload this will not be executed hence we need to use uviorn blog.main:app --reload
    return blog.create_blog(request,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db: Session=Depends(get_db)):
    return blog.delete_blog(id,db)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request:schemas.Blog, db: Session=Depends(get_db)):
    return blog.update_blog(id,request,db)

# @app.get('/blog',response_model=list[schemas.ShowBlog], tags=['blogs'])
# def get_all_blogs(db: Session=Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

@router.get('/{id}',response_model=schemas.ShowBlog)
def get_blog(id,db: Session=Depends(get_db)):
    return blog.get_blog(id,db)

