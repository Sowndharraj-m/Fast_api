from fastapi import FastAPI, Response, status, HTTPException , Depends
from httpx import post
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from database import engine, SessionLocal ,get_db
import models , schemas
from passlib.context import CryptContext
from routers import post , user , auth 

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
  try :
    conn = psycopg2.connect(host='localhost',database='fastapi_demo',user='postgres',password='Raj@2001',
                            cursor_factory=RealDictCursor)
    cursor =  conn.cursor()
    print("Database connection is done")
    break

  except Exception as error:
       print("conncetion database is failed")
       print("error:", error )
       time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
 return {"message": "Are you human"}

