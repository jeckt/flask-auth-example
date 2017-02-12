from flask_login import UserMixin

from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(35), index=True)
    #TODO(steve): make this encrpyted
    password_hash = db.Column(db.String(128))

    def get_id(self):
        try:
            return unicode(self.id)     # python 2
        except NameError:
            return str(self.id)         # python 3

    def verify_password(self, password):
        return self.password_hash == password

    def __repr__(self):
        return '<User %r>' % (self.username)


