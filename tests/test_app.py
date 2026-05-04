import json
import pytest
import app as app_module


@pytest.fixture
def client():
    app_module.app.config['TESTING'] = True

    # Reset state before each test
    app_module.tasks = []
    app_module.next_id = 1

    with app_module.app.test_client() as client:
        yield client


def test_get_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert json.loads(response.data) == []


def test_create_task(client):
    response = client.post('/tasks', json={"title": "Test task"})
    assert response.status_code == 201

    data = json.loads(response.data)
    assert data['title'] == "Test task"
    assert data['done'] is False


def test_get_task_by_id(client):
    client.post('/tasks', json={"title": "Sample"})
    response = client.get('/tasks/1')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == 1


def test_delete_task(client):
    client.post('/tasks', json={"title": "Delete me"})
    response = client.delete('/tasks/1')

    assert response.status_code == 200