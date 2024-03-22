from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .. import schemas,models,token
from sqlalchemy.orm import Session
from ..database import get_db
from ..hashing import Hash
from ..schemas import Token

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('')
def login(request:Annotated[OAuth2PasswordRequestForm,Depends()],db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect Password")
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")