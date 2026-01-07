from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Todos
import models
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_all(db: db_dependancy):
    return db.query(Todos).all()