from fastapi import FastAPI, Response, status, HTTPException , Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from database import engine, SessionLocal ,get_db
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()





# request GET method url:"/" (Order is not mater)

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    # rating: int 
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

@app.get("sqlalchemy")
def test_post(db:Session = Depends(get_db)):
   return {"status":"Success"}


@app.get("/post")
def receiving():
   cursor.execute("""select * from socialmedia_post""")
   post = cursor.fetchall()
   return{"data":post}

@app.post("/post")
def create_post(Text: Post):
    cursor.execute("""insert into socialmedia_post(title, content,published) values(%s,%s,%s)returning  *""", 
    (Text.title,Text.content,Text.published))

    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/post/{id}")
def get_post(id: int):

    cursor.execute(
        """SELECT * FROM socialmedia_post WHERE id = %s""",(str(id,)))
    test_post = cursor.fetchone()
    print(test_post)

    if test_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    return {"post_details": test_post}

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(
        """DELETE FROM socialmedia_post 
        WHERE id = %s RETURNING *""",
        (str(id),)
    )

    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    
@app.put("/post/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""
        UPDATE socialmedia_post
        SET title=%s, content=%s, published=%s
                   
        WHERE id=%s
        RETURNING *
    """, (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    return {"data": updated_post}

