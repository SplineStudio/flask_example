from project.database import db


class Photo(db.Model):
    __tablename__ = 'Photo'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('Property.id'))

    def __repr__(self):
        return '<Photo {}>'.format(self.file_name)