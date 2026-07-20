from models.user import User


def test_user_creation():
    user = User("Alex", "alex@gmail.com")
    assert user.name == "Alex"