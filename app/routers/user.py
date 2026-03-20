from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
import models , schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

router = APIRouter(
    prefix = "/users",
    tags=["users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def create_user (user:schemas.createuser,b:Session = Depends(get_db),response_model=schemas.userout):
  
    # Validate password length (bcrypt limit)
  if len(user.password.encode("utf-8")) > 72:
   raise ValueError("Password too long (max 72 bytes)")
    
  #hash the password  - user.password
  hashed_password = pwd_context.hash(user.password)
  user.password = hashed_password[:72]
  new_user = models.User(**user.model_dump())

  b.add(new_user)
  b.commit()
  b.refresh(new_user)

  return(new_user)

@router.get('/{id}',response_model=schemas.userout)
def get_user(id: int,b:Session = Depends(get_db)):
    user = b.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    return user