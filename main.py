from fastapi import FastAPI ,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

# request GET method url:"/" (Order is not mater)

class Post(BaseModel):
    Title : str
    content : str
    publised : bool = True
    rating: int 

my_post = [{"Title": "Title of post1","content":"content of post1","id":1},{"title":"I like Football","content":"my fav player is ronaldo","id":2}]

def find_id(id):
     for i in my_post:
         if i['id'] == id:
             return i

def find_index(id):
    for i , p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.get("/")
def login():

    return {"message": "Are you human"}

@app.get("/post")
def receiving():
   return{"date":my_post}

@app.post("/post")
def create_post(Text: Post):
    post_dict = Text.model_dump()
    post_dict["id"] = randrange(0,10000)
    my_post.append(post_dict)
    return {"data": post_dict}

# title , content from user 

# @app.get("/post/latest")
# def get_latest_post():
#     latest = my_post[len(my_post)-1]
#     return {"details":latest}

@app.get("/post/{id}")
def get_post(id: int):
    Text = find_id(int(id))
    if not Text:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"text with the id : {id} is not found")
    #  response.status_code = status.HTTP_404_NOT_FOUND
    #  return {"message":f"text with the id : {id} is not found"}
    return{"text_details":Text}

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
 index = find_index(id)
 if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The id = {id} is not exist")
 my_post.pop(index)
 return Response(status_code=status.HTTP_204_NO_CONTENT)
 

