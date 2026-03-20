from pydantic import BaseModel , EmailStr
from datetime import datetime

class Post(BaseModel):
    title : str
    content : str
    published : bool = True

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id : int
    created_at : datetime

    class Config:
        from_attributes = True

class createuser(BaseModel):
    email : EmailStr
    password : str

class userout(BaseModel):
    id : int 
    email : EmailStr
    created_at : datetime
    class Config:
        from_attributes = True

class userlogin(BaseModel):
    email : EmailStr
    password : str