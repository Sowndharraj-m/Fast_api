from fastapi import FastAPI,responses,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from  random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title:str
    content:str
    rating: Optional[int] = 4

mypost = [{"title" : "first post", "content" : "content of first post" ,"id" : 1},{"title" : "second post", "content" : "content of second post" ,"id" : 2}]

try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="Raj@2001"
    )
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print("Database connection was successful")
except Exception as e:
    print("Database connection failed")
    print("Error: ", e)


@app.get("/")
def read_root():
   return {"Hello": "Sowndharraj"}

@app.get("/posts")   
def get_posts():  
    cursor.execute('SELECT * FROM "FasT_API2"')
    posts = cursor.fetchall()       
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED) 
def create_posts(post: Post):
    cursor.execute('INSERT INTO "FasT_API2" (title,content,rating) VALUES (%s,%s,%s)',(post.title,post.content,post.rating))
    conn.commit()
    new_post = cursor.fetchone()  

    conn.commit()

    return {"data": new_post}

def find_post(id):
    for i, p in enumerate(mypost):
        if p["id"] == id:
            return i

@app.get("/posts/{id}")
def get_post(id: int):
   #print(type(id))
   cursor.execute('SELECT * FROM "FasT_API2" WHERE id = %s', (id,))
   print(cursor.rowcount)   
   post = cursor.fetchone()
   if post is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
       detail=f"Post with id:{id} was not found")
   return {"post_details":post}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('DELETE FROM "FasT_API2" WHERE id = %s', (id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute('UPDATE "FasT_API2" SET title = %s, content = %s, rating = %s WHERE id = %s', (post.title, post.content, post.rating, id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    post_dict = post.dict()
    post_dict['id'] = id
    return {"data": post_dict}
