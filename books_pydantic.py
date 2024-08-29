from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel,Field

app=FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int

    def __init__(self, id, title,author, description, rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating


# validation
class BookRequest(BaseModel):
    id:Optional[int]=Field(title="id is not needed")
    title:str=Field(min_length=3)
    author:str=Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=0,lt=6)

    class Config:
        json_schema_extra={
            "example":{
                "title":"a new book",
                "author":"codingwithragu",
                "description":"a new description",
                "rating":5
            }
        }

BOOKS=[
    Book(1,"computer science pro","code with roby","very nice book",5),
    Book(2,"Be fast with fastapi","code with roby","this is great book",5),
    Book(3,"Master end point","code with roby","very nice book",4),
    Book(4,"HP1","Author 1","very nice book",2),
    Book(5,"HP2","Author 2","very good book",3),
    Book(6,"HP3","Author 3","Book description",1),
]

@app.get("/books")
def read_all_books():
    return BOOKS


@app.post("/create-book")
def create_book(book_request:BookRequest):
    new_book=Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book:Book):
    if len(BOOKS)>0:
        book.id=BOOKS[-1].id+1
    else:
        book.id=1
    
    return book


