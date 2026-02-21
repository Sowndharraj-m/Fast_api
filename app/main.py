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

@app.post("/posts")    
def create_posts(post: Post):
    post_dict = post.dict()
    post_id = randrange(1,1000000)  
    post_dict['id'] = post_id
    mypost.append(post_dict)
    return {"data": post_dict}

def find_post(id):
    for i, p in enumerate(mypost):
        if p["id"] == id:
            return i

@app.get("/posts/{id}")
def get_post(id: int):
   #print(type(id))
   post = find_post(id)
   if post is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
       detail=f"Post with id:{id} was not found")
   return {"post_details":mypost[post]}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post(id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    mypost.pop(index)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    index = find_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    post_dict = post.dict()
    post_dict['id'] = id
    mypost[index] = post_dict
    return {"data": post_dict}
