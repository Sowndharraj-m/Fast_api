from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from  random import randrange

app = FastAPI()


class Post(BaseModel):
    title:str
    content:str
    rating: Optional[int] = 4

mypost = [{"title" : "first post", "content" : "content of first post" ,"id" : 1},{"title" : "second post", "content" : "content of second post" ,"id" : 2}]


@app.get("/")
def read_root():
   return {"Hello": "Sowndharraj"}

@app.get("/posts")   
def read_root():  
   return {"Hello": mypost}

@app.post("/posts")    
def create_posts(post: Post):
    post_dict = post.dict()
    post_id = randrange(1,1000000)  
    post_dict['id'] = post_id
    mypost.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id):
   print(id)
   return {"post_details":"this is the post for {id}"}

