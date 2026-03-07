from http.client import responses

from ..models import Todos
from .utils import *
from ..routers.admin import get_db
from ..routers.auth import get_current_user
from ..main import app

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authentication(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == 200
    assert response.json() == [
        {'complete': False, 'title': 'Learn FastAPI', 'description': 'Gotta learn everyday', 'id': 1, 'priority': 5,
         'owner_id': 1}
    ]

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204
    db =TestingLocalSession()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo Not Found"}