from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    published_date: int
    author: str
    description: str
    rating: int

    def __init__(self, id, title, published_date,author, description, rating):
        self.id = id
        self.title = title
        self.published_date = published_date
        self.author = author
        self.description = description
        self.rating  = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(description = "Id is not always needed", default = None)
    title: str = Field(min_length=3)
    published_date:int = Field(min_length=2)
    author: str = Field(min_length=2)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1,lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Book title",
                "published_date": "Published date",
                "author": "Book author",
                "description": "A book description",
                "rating": 5
            }
        }
    }

BOOKS = [
    Book(1, "Computer Science", 2012,"CC Coder", "Nice Book!", 5),
    Book(2, "Computer Science 1", 2013,"AB Coder", "Good Book!", 5),
    Book(3, "Computer Science 2", 2022,"CE Coder", "Better Book!", 3),
    Book(4, "Computer Science 3", 2023,"CD Coder", "Not so bad Book!", 5),
    Book(5, "Computer Science 4", 2025,"C Coder", "Very Nice Book!", 5),
]

def set_book_id(book : Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/")
async def get_book_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break

@app.get("/books/published/{published_date}")
async def get_by_published_date(published_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(set_book_id(new_book))
