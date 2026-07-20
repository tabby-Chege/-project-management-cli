import argparse
import os

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import load_data, save_data

DATA_FILE = "data/users.json"


def get_users():
    users = load_data(DATA_FILE)
    if users is None:
        return []
    return users


def save_users(users):
    save_data(DATA_FILE, users)


def next_user_id(users):
    if not users:
        return 1
    return max(user["id"] for user in users) + 1


def find_user(users, user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def find_project(user, title):
    for project in user["projects"]:
        if project["title"].lower() == title.lower():
            return project
    return None


def add_user(args):
    users = get_users()

    # Check for duplicate email
    for user in users:
        if user["email"].lower() == args.email.lower():
            print("A user with this email already exists.")
            return

    user_data = {
        "id": next_user_id(users),
        "name": args.name,
        "email": args.email,
        "projects": []
    }

    users.append(user_data)

    save_users(users)

    print(f"User '{args.name}' added successfully.")



def add_project(args):
    users = get_users()

    user = find_user(users, args.user_id)

    if user is None:
        print("User not found.")
        return

    # Prevent duplicate projects
    for project in user["projects"]:
        if project["title"].lower() == args.title.lower():
            print("Project already exists.")
            return

    project = {
        "title": args.title,
        "description": args.description,
        "due_date": args.due_date,
        "tasks": []
    }

    user["projects"].append(project)

    save_users(users)

    print(f"Project '{args.title}' added successfully.")


def list_projects(args):
    users = get_users()

    found = False

    for user in users:
        if user["projects"]:
            print(f"\nProjects for {user['name']}")
            print("-" * 50)

            for project in user["projects"]:
                print(f"Title: {project['title']}")
                print(f"Description: {project['description']}")
                print(f"Due Date: {project['due_date']}")
                print()

            found = True

    if not found:
        print("No projects found.")  
def add_task(args):
    users = get_users()

    for user in users:
        project = find_project(user, args.project)

        if project:

            # Prevent duplicate task titles in the same project
            for task in project["tasks"]:
                if task["title"].lower() == args.title.lower():
                    print("Task already exists.")
                    return

            task = {
                "title": args.title,
                "assigned_to": args.assigned_to,
                "status": False
            }

            project["tasks"].append(task)

            save_users(users)

            print(f"Task '{args.title}' added successfully.")
            return

    print("Project not found.")


def complete_task(args):
    users = get_users()

    for user in users:
        project = find_project(user, args.project)

        if project:
            for task in project["tasks"]:
                if task["title"].lower() == args.title.lower():
                    task["status"] = True
                    save_users(users)

                    print("Task marked as complete.")
                    return

            print("Task not found.")
            return

    print("Project not found.")
def main():
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool"
    )

    subparsers = parser.add_subparsers(dest="command")

    # ----------------------
    # add-user
    # ----------------------
    add_user_parser = subparsers.add_parser(
        "add-user",
        help="Add a new user"
    )

    add_user_parser.add_argument("--name", required=True)
    add_user_parser.add_argument("--email", required=True)
    add_user_parser.set_defaults(func=add_user)

    # ----------------------
    # list-users
    # ----------------------
    list_user_parser = subparsers.add_parser(
        "list-users",
        help="Display all users"
    )

    list_user_parser.set_defaults(func=list_users)

    # ----------------------
    # add-project
    # ----------------------
    add_project_parser = subparsers.add_parser(
        "add-project",
        help="Add project to a user"
    )

    add_project_parser.add_argument(
        "--user-id",
        type=int,
        required=True
    )

    add_project_parser.add_argument(
        "--title",
        required=True
    )

    add_project_parser.add_argument(
        "--description",
        required=True
    )

    add_project_parser.add_argument(
        "--due-date",
        required=True
    )

    add_project_parser.set_defaults(func=add_project)

    # ----------------------
    # list-projects
    # ----------------------
    list_project_parser = subparsers.add_parser(
        "list-projects",
        help="Display all projects"
    )

    list_project_parser.set_defaults(func=list_projects)

    # ----------------------
    # add-task
    # ----------------------
    add_task_parser = subparsers.add_parser(
        "add-task",
        help="Add task to a project"
    )

    add_task_parser.add_argument(
        "--project",
        required=True
    )

    add_task_parser.add_argument(
        "--title",
        required=True
    )

    add_task_parser.add_argument(
        "--assigned-to",
        required=True,
        dest="assigned_to"
    )

    add_task_parser.set_defaults(func=add_task)

    # ----------------------
    # complete-task
    # ----------------------
    complete_parser = subparsers.add_parser(
        "complete-task",
        help="Mark task complete"
    )

    complete_parser.add_argument(
        "--project",
        required=True
    )

    complete_parser.add_argument(
        "--title",
        required=True
    )

    complete_parser.set_defaults(func=complete_task)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()