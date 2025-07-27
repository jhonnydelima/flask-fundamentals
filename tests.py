import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'
tasks = []

def test_create_task():
  response = requests.post(f'{BASE_URL}/tasks', json={
    'title': 'Test Task',
    'description': 'This is a test task'
  })
  assert response.status_code == 201
  response_json = response.json()
  assert "message" in response_json
  assert "id" in response_json
  tasks.append(response_json['id'])

def test_get_tasks():
  response = requests.get(f'{BASE_URL}/tasks')
  assert response.status_code == 200
  response_json = response.json()
  assert 'tasks' in response_json
  assert 'total_tasks' in response_json
  assert len(response_json['tasks']) == len(tasks)

def test_get_task():
  if tasks:
    task_id = tasks[0]
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert task_id == response_json['id']

def test_update_task():
  if tasks:
    task_id = tasks[0]
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json={
      'title': 'Updated Task',
      'description': 'This task has been updated'
    })
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json

    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['title'] == 'Updated Task'
    assert response_json['description'] == 'This task has been updated'

def test_toggle_task_completion():
  if tasks:
    task_id = tasks[0]
    response = requests.patch(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json

    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['completed'] == True

def test_delete_task():
  if tasks:
    task_id = tasks[0]

    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200

    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json

    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 404