import typer
import json
from typing import List

app = typer.Typer()

TASKS_FILE = "tasks.json"

def load_tasks() -> List[str]:
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks: List[str]):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

@app.command()
def add_task(task: str):
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{task}' added.")
    
@app.command()
def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks available.")
    else:
        print("Tasks:")
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task}")
            
@app.command()
def remove_task(task_number: int):
    tasks = load_tasks()
    if 1 <= task_number <= len(tasks):
        task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        print(f"Marked '{task}' as done.")
    else:
        print("Invalid task number.")
        
if __name__ == "__main__":
    app()