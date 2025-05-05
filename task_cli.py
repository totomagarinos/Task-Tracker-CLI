#!/usr/bin/env python3

import argparse
from datetime import datetime
import json
import os
import sys

# File to store tasks
TASKS_FILE = "tasks.json"

def load_tasks():
  # Load tasks from the tasks file.
  if os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "r") as f:
      return json.load(f)
  else:
    with open(TASKS_FILE, "w") as f:
      json.dump([], f)

def save_tasks(tasks):
  # Save tasks to the tasks file.
  with open(TASKS_FILE, "w") as f:
    json.dump(tasks, f, indent=2)

def add_task(description):
  # Add a new task.
  tasks = load_tasks()
  task_id = len(tasks) + 1
  now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  
  task = {
    "id": task_id,
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
  # Delete a task.
  tasks = load_tasks()

  for task in tasks:
    if task["id"] == int(id):
      tasks.remove(task)
      save_tasks(tasks)
      print(f'Task {id} deleted')
      return
  print(f'Task with ID {id} not found')

  # Reassign IDs to keep the sequential
  for i, task in enumerate(tasks, 1):
      task["id"] = i

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

def print_tasks(tasks):
  if not tasks:
    print('No tasks found')
    return
  
  print(f"{'ID':<5} {'Description':<32} {'Status':<15} {'Created at':<25} {'Updated at':<25}")
  print('-' * 120)
      
  for task in tasks:
    print(
      f'{str(task["id"]):<5}'
      f'{(task["description"]):<35}'
      f'{(task["status"]):<15}'
      f'{(task["created_at"]):<25}'
      f'{(task["updated_at"]):<25}'
    )

def list_tasks():
  # List all tasks
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
  parser = argparse.ArgumentParser(description="CLI Task Manager")
  subparsers = parser.add_subparsers(dest="command", help="Command to run")

  # Add task
  add_parser = subparsers.add_parser("add", help="Add a new task")
  add_parser.add_argument("description", help="Task description")

  # Update task
  update_parser = subparsers.add_parser("update", help="Update a task")
  update_parser.add_argument('task_id', type=int, help="ID of the task to update")
  update_parser.add_argument('description', help="Updated task description")

  # Delete task
  delete_parser = subparsers.add_parser("delete", help="Delete a task")
  delete_parser.add_argument('task_id', type=int, help="ID of the task to delete")

  # List tasks
  list_parser = subparsers.add_parser("list", help="List all tasks")
  list_parser.add_argument(
    "filter",
    choices=["all", "done", "todo", "in-progress"],
    nargs="?",
    default="all",
    help="Filter tasks")
  
  # List done tasks

  # List todo tasks

  # List in progress tasks

  args = parser.parse_args()

  if args.command == "add":
    add_task(args.description)
  elif args.command == "update":
    update_task(args.task_id, args.description)
  elif args.command == "delete":
    delete_task(args.task_id)
  elif args.command == "list":
    if args.filter == "all":
      list_tasks()
    elif args.filter == "done":
      list_done_tasks()
    elif args.filter == "in-progress":
      list_in_progress_tasks()
    elif args.filter == "todo":
      list_not_done_tasks()
  else:
    parser.print_help()

if __name__ == "__main__":
  main()