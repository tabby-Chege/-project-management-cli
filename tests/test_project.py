from models.project import Project


def test_project_creation():
    project = Project("Hospital", "Manage patients", "2026-09-30")
    assert project.title == "Hospital"