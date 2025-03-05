import pytest
import os
import sqlite3
from app import app, init_db, get_db_connection, add_task, get_tasks, delete_task

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
    if os.path.exists("todo.db"):
        os.remove("todo.db")

def test_init_db(client):
    assert os.path.exists("todo.db")
    conn = get_db_connection()
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
    assert cursor.fetchone() is not None
    conn.close()

def test_add_task(client):
    add_task("Test Task")
    tasks = get_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test Task"

def test_delete_task(client):
    add_task("Test Task")
    tasks = get_tasks()
    delete_task(tasks[0]["id"])
    tasks = get_tasks()
    assert len(tasks) == 0