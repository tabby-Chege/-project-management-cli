class Task:
    def __init__(self, title, assigned_to):
        self.title = title
        self.assigned_to = assigned_to
        self.status = False

    def complete_task(self):
        self.status = True

    def __str__(self):
        status = "Complete" if self.status else "Incomplete"
        return (
            f"Task: {self.title}\n"
            f"Assigned To: {self.assigned_to}\n"
            f"Status: {status}"
        )