from project.database import db


class Property(db.Model):
    __tablename__ = 'Property'

    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('Dir_system.id'), nullable=False)
    inner_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    country = db.Column(db.String(120))
    city = db.Column(db.String(120))
    district = db.Column(db.String(120))
    zip_code = db.Column(db.String(30))
    currency = db.Column(db.String(30))
    photo_url = db.Column(db.String(255))
    price = db.Column(db.Integer)
    min_stay = db.Column(db.Integer)
    number_of_guests = db.Column(db.Integer)
    size = db.Column(db.Integer)

    flat_id = db.Column(db.Integer, db.ForeignKey('Flat.id'))
    local_user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __repr__(self):
        return '<Property {}>'.format(self.name)
