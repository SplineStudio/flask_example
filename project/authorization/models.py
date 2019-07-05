from project.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(255))
    password = db.Column(db.String(120))
    code_recovery = db.Column(db.String(30), nullable=True)
    date_code_recovery = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.first_name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
