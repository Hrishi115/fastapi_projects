from fastapi.params import Query, Body
from pydantic import Field, BaseModel
from fastapi import FastAPI, HTTPException, Path
from datetime import datetime
from starlette import status

app = FastAPI()

class Sum(BaseModel):
    a: int
    b: int

@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status":"ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/square/{num}", status_code=status.HTTP_200_OK)
def square(num: int = Path(..., gt = 0, description="Postive integer only")):
    return {"result": num * num }

@app.post("/sum", status_code=status.HTTP_201_CREATED)
def sum(number: Sum):
    return {"result" : number.a + number.b}

@app.get("/search/", status_code=status.HTTP_200_OK)
def search(q: str = Query(...), limit :int = Query(10, le=50)):
    return {
        "query": q,
        "limit": limit
    }

@app.post("/echo", status_code=status.HTTP_200_OK)
def echo(user_msg: dict = Body(...)):
    return user_msg