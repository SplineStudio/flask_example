from project.database import db


class Flat(db.Model):
    __tablename__ = 'Flat'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __repr__(self):
        return '<Flat {}>'.format(self.name)

