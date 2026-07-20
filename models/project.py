class Project:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def __str__(self):
        return (
            f"Project: {self.title}\n"
            f"Description: {self.description}\n"
            f"Due Date: {self.due_date}"
        )