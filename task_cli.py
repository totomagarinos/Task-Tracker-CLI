from datetime import datetime
import json
import os
import sys

TASKS_FILE = "tasks.json"

def ensure_json_file_exists():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)

def load_tasks():
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def generate_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(description):
    tasks = load_tasks()
    now = datetime.now().isoformat()
    
    task = {
        "id": generate_id(tasks),
        "description": description,
        "status": "todo",
        "created_at": now,
        "updated_at": now
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task added successfully (ID: {task["id"]})')


def update_task(id, description):
    tasks = load_tasks()
    now = datetime.now().isoformat()
    updated = False

    for task in tasks:
        if task["id"] == int(id):
            task["description"] = description
            task["updated_at"] = now
            updated = True
            break

    if updated:
        save_tasks(tasks)
        print(f'Task {id} updated successfully')
    else:
        print(f'Task with ID {id} not found')


if __name__ == "__main__":
    ensure_json_file_exists()

    if len(sys.argv) >= 3 and sys.argv[1] == "add":
        description = sys.argv[2]
        add_task(description)
    elif sys.argv[1] == "update":
        id = sys.argv[2]
        description = sys.argv[3]
        update_task(id, description)
