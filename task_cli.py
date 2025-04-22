from datetime import datetime
import json
import os

TASKS_FILE = "tasks.json"

def ensure_json_file_exists():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)


def load_tasks():
    with open(TASKS_FILE, "r") as f:
        json.load(f)


def generate_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks)


def add_task(description: str):
    tasks = load_tasks()
    now = datetime.now()
    
    task = {
        "id": generate_id(),
        "description": description,
        "status": "todo",
        "created_at": now,
        "updated_at": now
    }

    tasks.append(task)