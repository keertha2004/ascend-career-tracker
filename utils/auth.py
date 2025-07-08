from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_row):
        self.id = user_row['id']
        self.username = user_row['username']
        self.email = user_row['email']
        self.password_hash = user_row['password_hash']
