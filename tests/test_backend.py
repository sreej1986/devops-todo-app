# tests/test_backend.py
import pytest
from backend.app import app, todos # Import app and todos from your Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear todos before each test to ensure isolation
        todos.clear() 
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"To-Do Backend is Running!" in response.data

def test_get_empty_todos(client):
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.json == []

def test_add_todo(client):
    response = client.post('/todos', json={'task': 'Learn DevOps'})
    assert response.status_code == 201
    assert response.json['task'] == 'Learn DevOps'
    assert response.json['completed'] == False
    assert 'id' in response.json

    # Verify it's added
    response = client.get('/todos')
    assert len(response.json) == 1
    assert response.json[0]['task'] == 'Learn DevOps'

def test_add_todo_missing_task(client):
    response = client.post('/todos', json={})
    assert response.status_code == 400
    assert "Task is required" in response.json['error']

def test_update_todo(client):
    # Add a todo first
    add_response = client.post('/todos', json={'task': 'Buy groceries'})
    todo_id = add_response.json['id']

    # Update it
    update_response = client.put(f'/todos/{todo_id}', json={'completed': True})
    assert update_response.status_code == 200
    assert update_response.json['completed'] == True
    assert update_response.json['task'] == 'Buy groceries' # Task should remain same

    # Verify the update
    get_response = client.get(f'/todos/{todo_id}') # Note: Flask test client doesn't have a direct get by ID, need to fetch all and filter or add an endpoint for it if not doing so
    # For simplicity, we just check the update response itself, or fetch all todos

    all_todos = client.get('/todos').json
    found_todo = next((t for t in all_todos if t['id'] == todo_id), None)
    assert found_todo['completed'] == True


def test_delete_todo(client):
    # Add a todo first
    add_response = client.post('/todos', json={'task': 'Clean room'})
    todo_id = add_response.json['id']

    # Delete it
    delete_response = client.delete(f'/todos/{todo_id}')
    assert delete_response.status_code == 204

    # Verify it's deleted
    response = client.get('/todos')
    assert response.json == []

def test_delete_non_existent_todo(client):
    response = client.delete('/todos/non-existent-id')
    assert response.status_code == 404
    assert "To-Do not found" in response.json['error']
