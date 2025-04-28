#!/usr/bin/env python3

from datetime import datetime
import json
import os
import sys

TASKS_FILE = "tasks.json"

# SECONDARY FUNCTIONS
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

def print_tasks(tasks):
    if not tasks:
        print('Not tasks found')
        return
    print(f'{'ID':<5} {'Description':<32} {'Status':<15} {'Created at':<25} {'Updated at':<25}')
    print('-' * 120)
        
    for task in tasks:
        print(
            f'{str(task["id"]):<5}'
            f'{(task["description"]):<35}'
            f'{(task["status"]):<15}'
            f'{(task["created_at"]):<25}'
            f'{(task["updated_at"]):<25}'
        )

# MAIN FUNCTIONS
def add_task(description):
    tasks = load_tasks()
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
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
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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

def delete_task(id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == int(id):
            tasks.remove(task)
            save_tasks(tasks)
            print(f'Task {id} deleted')
            return
    print(f'Task with ID {id} not found')

def mark_in_progress(id):
    tasks = load_tasks()
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    updated = False

    for task in tasks:
        if task["id"] == int(id):
            task["status"] = "in progress"
            task["updated_at"] = now
            updated = True
            break
    
    if updated:
        save_tasks(tasks)
        print(f'Task {id} in progress')
    else:
        print(f'Task with ID {id} not found')

def mark_done(id):
    tasks = load_tasks()
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    updated = False

    for task in tasks:
        if task["id"] == int(id):
            task["status"] = "done"
            task["updated_at"] = now
            updated = True
            break
    
    if updated:
        save_tasks(tasks)
        print(f'Task {id} done')
    else:
        print(f'Task with ID {id} not found')

def list_tasks():
    tasks = load_tasks()
    print_tasks(tasks)

def list_done_tasks():
    tasks = load_tasks()
    done_tasks = [task for task in tasks if task["status"] == "done"]
    print_tasks(done_tasks)

def list_not_done_tasks():
    tasks = load_tasks()
    not_done_tasks = [task for task in tasks if task["status"] == "todo"]
    print_tasks(not_done_tasks)

def list_in_progress_tasks():
    tasks = load_tasks()
    in_progress_tasks = [task for task in tasks if task["status"] == "in progress"]
    print_tasks(in_progress_tasks)


def main():
    ensure_json_file_exists()

    if len(sys.argv) >= 3 and sys.argv[1] == "add":
        description = sys.argv[2]
        add_task(description)
    elif sys.argv[1] == "update":
        id = sys.argv[2]
        description = sys.argv[3]
        update_task(id, description)
    elif sys.argv[1] == "mark-in-progress":
        id = sys.argv[2]
        mark_in_progress(id)
    elif sys.argv[1] == "mark-done":
        id = sys.argv[2]
        mark_done(id)
    elif sys.argv[1] == "delete":
        id = sys.argv[2]
        delete_task(id)
    elif sys.argv[1] == "list":
        if len(sys.argv) == 2:
            list_tasks()
        elif sys.argv[2] == "done":
            list_done_tasks()
        elif sys.argv[2] == "in-progress":
            list_in_progress_tasks()
        elif sys.argv[2] == "todo":
            list_not_done_tasks()
        else:
            print(f'Unknown list filter: {sys.argv[2]}')

if __name__ == "__main__":
    main()