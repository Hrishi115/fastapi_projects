from typing import Optional
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field
from starlette import status
import datetime

app = FastAPI()

class MultiplyRequest(BaseModel):
    a: int
    b: int
    round_result: Optional[bool] = Field(default=False)

class Sum(BaseModel):
    x: int
    y: int

class User(BaseModel):
    username: str
    age: int = Field(gt=0)

class Products(BaseModel):
    price: int = Field(gt=0)

@app.get("/ping", status_code=status.HTTP_200_OK)
def ping():
    return {
        "message": "pong",
        "utc_time": datetime.datetime.now()
    }

@app.get("/double/{value}", status_code=status.HTTP_200_OK)
def double(value: int = Path(..., gt=0)):
    return {
        "result": value * 2
    }

@app.post("/add", status_code=status.HTTP_200_OK)
def add(number: Sum):
    return {"sum": number.x + number.y}

@app.post("/multiply", status_code=status.HTTP_201_CREATED)
def multiply(body: MultiplyRequest):
    result = body.a * body.b
    if body.round_result == True:
        return {"result": round(result, 2)}
    else:
        return {"result": result}

@app.get("/items/", status_code=status.HTTP_200_OK)
async def read_items(limit: int = Query(default=5, le=20)):
    return {"limit_used": limit}

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    return {
        "username": user.username,
        "age": user.age
            }

@app.post("/mirror", status_code=status.HTTP_201_CREATED)
async def mirror(body: dict = Body(...)):
    return body

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def get_all_posts(post_id: int = Path(gt=0)):
    return {
        "post_id": post_id
    }

@app.get("/posts/", status_code=status.HTTP_200_OK)
async def get_post_by_author(author_name: str = Query()):
    return {
        "author name": author_name
    }

@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
async def product(product_id: int = Path(gt=0), bod: Products = Body(...)):
    return {
        "product id": product_id,
        "price": bod.price
    }

@app.get("/find/", status_code=status.HTTP_200_OK)
async def find(q: str, page: int = Query(default=1, ge=1)):
    return {
        "q": q,
        "page": page
    }