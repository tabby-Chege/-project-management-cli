from models.task import Task


def test_task_creation():
    task = Task("Database", "Alex")
    assert task.title == "Database"