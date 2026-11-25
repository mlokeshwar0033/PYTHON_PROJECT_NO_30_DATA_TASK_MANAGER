# PROJECT NO. 30
# DAILY TASK MANAGER
# Language: Python 3

import os
from datetime import datetime

# Store tasks.txt in the same folder as this Python file
TASKS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tasks.txt"
)

VALID_PRIORITIES = ["High", "Medium", "Low"]


# 1. LOAD TASKS FROM FILE
def load_tasks():
    tasks = []

    if not os.path.exists(TASKS_FILE):
        return tasks

    with open(TASKS_FILE, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = [p.strip() for p in line.split("|")]

            if len(parts) != 5:
                continue

            task = {
                "id": parts[0],
                "title": parts[1],
                "priority": parts[2],
                "due": parts[3],
                "status": parts[4]
            }

            tasks.append(task)

    return tasks


# 2. SAVE TASKS TO FILE
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        for task in tasks:
            file.write(
                f"{task['id']} | {task['title']} | "
                f"{task['priority']} | {task['due']} | "
                f"{task['status']}\n"
            )


# 3. GENERATE UNIQUE TASK ID
def next_id(tasks):
    highest = 100

    for task in tasks:
        number = int(task["id"][1:])
        highest = max(highest, number)

    return f"T{highest + 1}"


# 4. VALIDATE DATE
def valid_date(date_text):
    try:
        parsed_date = datetime.strptime(
            date_text, "%Y-%m-%d"
        )

        return parsed_date.strftime("%Y-%m-%d") == date_text

    except ValueError:
        return False


# 5. ADD NEW TASK
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
        "status": "Pending"
    }

    tasks.append(task)
    save_tasks(tasks)

    print("Task added.")

    print(
        f"{task['id']} | {task['title']} | "
        f"{task['priority']} | {task['due']} | "
        f"{task['status']}"
    )


# 6. VIEW TASKS BY PRIORITY
def view_by_priority(tasks):
    if not tasks:
        print("No tasks available.")
        return

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    sorted_tasks = sorted(
        tasks,
        key=lambda task: priority_order.get(
            task["priority"], 4
        )
    )

    for task in sorted_tasks:
        print(
            f"{task['id']} | {task['title']} | "
            f"{task['priority']} | {task['due']}"
        )


# 7. SHOW PENDING TASKS
def show_pending(tasks):
    pending_tasks = [
        task for task in tasks
        if task["status"] == "Pending"
    ]

    if not pending_tasks:
        print("No pending tasks. You are all caught up!")
        return

    for task in pending_tasks:
        print(
            f"{task['id']} | {task['title']} | "
            f"{task['priority']} | {task['due']} | "
            f"{task['status']}"
        )


# 8. COMPLETE A TASK
def complete_task(tasks):
    task_id = input("Task ID: ").strip().upper()

    for task in tasks:
        if task["id"] == task_id:

            if task["status"] == "Done":
                print(f"Task {task_id} is already completed.")
                return

            task["status"] = "Done"
            save_tasks(tasks)

            remaining = sum(
                1 for t in tasks
                if t["status"] == "Pending"
            )

            print(
                f"Task {task_id} marked as done. "
                f"Pending tasks: {remaining}"
            )
            return

    print(f"Task {task_id} not found.")


# 9. DISPLAY MENU
def print_menu():
    print("\n=== Daily Task Manager ===")
    print("1. Add task")
    print("2. View tasks by priority")
    print("3. Show pending tasks")
    print("4. Complete a task")
    print("5. Exit")


# 10. MAIN FUNCTION
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
            print("Thank you for using Daily Task Manager!")
            break

        else:
            print("Invalid option. Please pick 1 to 5.")


# PROGRAM STARTS HERE
if __name__ == "__main__":
    main()
