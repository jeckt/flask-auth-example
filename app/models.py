from flask_login import UserMixin

from app import db

class User(UserMixin):
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
                     "JaneDoe": ("JaneDoe", "Jane")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls, id):
        d = cls.user_database.get(id)
        return User(d[0], d[1])

    @classmethod
    def verify_password(cls, username, password):
        if username in cls.user_database:
            return cls.user_database[username][1] == password

        return False
