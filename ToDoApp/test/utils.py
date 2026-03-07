from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from fastapi.testclient import TestClient
from sqlalchemy import text
from ..main import app
import pytest
from ..models import Todos

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool,)

TestingLocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingLocalSession()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username": "Hrishi_test", "id": 1, "user_role":"admin"}

client = TestClient(app)

@pytest.fixture()
def test_todo():
    todo = Todos(
        title = "Learn FastAPI",
        description = "Gotta learn everyday",
        id = 1,
        priority = 5,
        owner_id = 1,
        complete = False
    )

    db = TestingLocalSession()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()