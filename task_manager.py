# Daily Task Manager
# Simple console app to track tasks with priority and due dates.

import os
from datetime import datetime

TASKS_FILE = "tasks.txt"
VALID_PRIORITIES = ["High", "Medium", "Low"]
NEXT_ID = 101  # task ids start from T101


def load_tasks():
    """Read tasks from the file into a list of dicts."""
    tasks = []
    if not os.path.exists(TASKS_FILE):
        return tasks
    with open(TASKS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # line looks like: T101 | Submit report | High | 2026-10-15 | Pending
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 4:
                continue  # skip badly formed lines
            task = {
                "id": parts[0],
                "title": parts[1],
                "priority": parts[2],
                "due": parts[3],
                "status": parts[4] if len(parts) > 4 else "Pending",
            }
            tasks.append(task)
    return tasks


def save_tasks(tasks):
    """Write every task back to the file."""
    with open(TASKS_FILE, "w") as f:
        for t in tasks:
            f.write("{} | {} | {} | {} | {}\n".format(
                t["id"], t["title"], t["priority"], t["due"], t["status"]))


def next_id(tasks):
    # ids are like T101, T102... keep counting from the highest one seen
    highest = 100
    for t in tasks:
        num = int(t["id"][1:])
        if num > highest: 
            highest = num
    return "T" + str(highest + 1)


def valid_date(text):
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_task(tasks):
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    priority = input("Priority: ").strip()
    if priority not in VALID_PRIORITIES:
        print("Invalid priority. Enter High, Medium or Low.")
        return
    due = input("Due: ").strip()
    if not valid_date(due):
        print("Invalid date. Use YYYY-MM-DD.")
        return
    task = {
        "id": next_id(tasks),
        "title": title,
        "priority": priority,
        "due": due,
        "status": "Pending",
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")
    print("{} | {} | {} | {} | {}".format(
        task["id"], task["title"], task["priority"], task["due"], task["status"]))


def view_by_priority(tasks):
    # order: High first, then Medium, then Low
    order = {"High": 0, "Medium": 1, "Low": 2}
    sorted_tasks = sorted(tasks, key=lambda t: order.get(t["priority"], 3))
    for t in sorted_tasks:
        print("{} | {} | {} | {} | {}".format(
            t["id"], t["title"], t["priority"], t["due"], t["status"]))


def show_pending(tasks):
    pending = [t for t in tasks if t["status"] == "Pending"]
    if not pending:
        print("No pending tasks. You are all caught up!")
        return
    for t in pending:
        print("{} | {} | {} | {} | {}".format(
            t["id"], t["title"], t["priority"], t["due"], t["status"]))


def complete_task(tasks):
    tid = input("Task ID: ").strip().upper()
    for t in tasks:
        if t["id"] == tid:
            t["status"] = "Done"
            save_tasks(tasks)
            remaining = len([x for x in tasks if x["status"] == "Pending"])
            print("Task {} marked as done. Pending tasks: {}".format(tid, remaining))
            return
    print("Task {} not found.".format(tid))


def print_menu():
    print()
    print("=== Daily Task Manager ===")
    print("1. Add task")
    print("2. View tasks by priority")
    print("3. Show pending tasks")
    print("4. Complete a task")
    print("5. Exit")


def main():
    tasks = load_tasks()
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_by_priority(tasks)
        elif choice == "3":
            show_pending(tasks)
        elif choice == "4":
            complete_task(tasks)
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("Please pick 1 to 5.")


if __name__ == "__main__":
    main()
