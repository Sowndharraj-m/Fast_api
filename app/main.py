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

@app.get("/")
def root():
 return {"message": "Are you human"}

@app.get("/post",response_model=list[schemas.PostResponse])
def receiving(db:Session = Depends(get_db)):
#    cursor.execute("""select * from socialmedia_post""")
#    post = cursor.fetchall()
 posts = db.query(models.post)
 return posts

@app.post("/post",response_model=schemas.PostResponse)
def create_post(Text: schemas.PostBase,b:Session = Depends(get_db)):
    # cursor.execute("""insert into socialmedia_post(title, content,published) values(%s,%s,%s)returning  *""", 
    # (Text.title,Text.content,Text.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.post(**Text.model_dump())

    b.add(new_post)
    b.commit()
    b.refresh(new_post)
    
    return new_post


@app.get("/post/{id}")
def get_post(id: int,b:Session = Depends(get_db),response_model=schemas.PostResponse):

    # cursor.execute(
    #     """SELECT * FROM socialmedia_post WHERE id = %s""",(str(id,)))
    # test_post = cursor.fetchone()
    # print(test_post)
    post = b.query(models.post).filter(models.post.id==id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    return {"post_details": post}

@app.delete("/post/{id}", status_code=status.HTTP_200_OK,response_model=schemas.PostResponse)
def delete_post(id: int , b:Session = Depends(get_db)):
    post_query = b.query(models.post).filter(models.post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist")
    post_query.delete(synchronize_session=False)
    b.commit()
    
@app.put("/post/{id}")
def update_post(id: int, post: schemas.PostResponse,b:Session = Depends(get_db),response_model=[schemas.PostResponse]):
    post_query = b.query(models.post).filter(models.post.id == id)
    existing_post = post_query.first()
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    post_query.update(post.model_dump(),synchronize_session=False)
    b.commit()
    return "post updated successfully"

