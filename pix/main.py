from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
import os
import json
from pydantic import BaseModel
from typing import Optional, Literal
from fastapi.encoders import jsonable_encoder
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

# Book Model
class Book(BaseModel):
    name: str
    price: float
    genre: Literal["fiction", "non-fiction"]
    book_id: Optional[str] = uuid4().hex

BOOKS_FILE = "books.json"
BOOK_DATABASE = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOK_DATABASE = json.load(f)

@app.get("/")
async def root():
    return {"message": "Welcome to my bookstore!"}

@app.get("/list-books")
async def list_books():
    return {"books": BOOK_DATABASE}

@app.get("/book-by-index/{index}")
async def book_by_index(index: int):
    if index < 0 or index > len(BOOK_DATABASE):
        raise HTTPException(404, f"Index {index} is out of range {len(BOOK_DATABASE)}.")
    else:
        return {"book": BOOK_DATABASE[index]}

@app.get("/get-random-books")
async def get_random_book():
    return random.choice(BOOK_DATABASE)

@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOK_DATABASE, f)
    return {"message": f"Book {book} was added.", "book_id": book.book_id}

@app.get("/get-book")
async def get_book(book_id: str):
    for book in BOOK_DATABASE:
        if book["book_id"] == book_id:
            return book

    raise HTTPException(404, f"Book not found: {book_id}") 

# /
# /list-books
# /book-by-index/{index} /book-by-index/0
# /get-random-book
# /add-book
# /get-book?id=...

#Making a change...
