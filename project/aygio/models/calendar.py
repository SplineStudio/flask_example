from flask_restful import fields, marshal_with
from project.database import db


class Calendar(db.Model):
    __tablename__ = 'Calendar'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('Property.id'), nullable=False)
    system_id = db.Column(db.Integer, db.ForeignKey('Dir_system.id'), nullable=False)
    availability = db.Column(db.String(30))
    price = db.Column(db.Integer)
    currency = db.Column(db.String(30))
    start_date = db.Column(db.String(30))
    end_date = db.Column(db.String(30))

    def __repr__(self):
        return '<Calendar {}, {}>'.format(self.id,
                                          self.property_id)

    formater={
        'id': fields.Integer,
        'property_id': fields.Integer,
        'system_id': fields.Integer,
        'availability': fields.String,
        'price': fields.Integer,
        'currency': fields.String,
        'start_date': fields.String,
        'end_date': fields.String,
    }

    @staticmethod
    @marshal_with(formater)
    def calendar_by_json(calendar):
        return calendar


class GuestInfo(db.Model):
    __tablename__ = 'GuestInfo'

    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(db.Integer, db.ForeignKey('Calendar.id'), nullable=False)
    system_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(30))
    phone_number = db.Column(db.String(30))
    guests = db.Column(db.Integer)
    nights = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)
    currency = db.Column(db.String(30))
    from_time = db.Column(db.String(30))
    to_time = db.Column(db.String(30))

    def __repr__(self):
        return '<GuestInfo {}, {} user_name={} nights={}>'.format(self.id,
                                                                  self.calendar_id,
                                                                  self.user_name,
                                                                  self.nights)

    formater = {
        'id': fields.Integer,
        'calendar_id': fields.Integer,
        'user_name': fields.String,
        'phone_number': fields.String,
        'guests': fields.Integer,
        'nights': fields.Integer,
        'total_cost': fields.String,
        'currency': fields.String,
    }

    @staticmethod
    @marshal_with(formater)
    def guest_by_json(renter):
        return renter


class Rental(db.Model):
    __tablename__ = 'Rental'

    id = db.Column(db.Integer, primary_key=True)
    flat_id = db.Column(db.Integer, db.ForeignKey('Flat.id'), nullable=False)
    user_name = db.Column(db.String(30))
    phone_number = db.Column(db.String(30))
    guests = db.Column(db.Integer)
    from_date = db.Column(db.String(30))
    to_date = db.Column(db.String(30))
    from_time = db.Column(db.String(30))
    to_time = db.Column(db.String(30))

    def __repr__(self):
        return '<Rental {}, user_name={} nights={}>'.format(self.id,
                                                            self.user_name,
                                                            self.nights)

    formater = {
        'id': fields.Integer,
        'flat_id': fields.Integer,
        'user_name': fields.String,
        'phone_number': fields.String,
        'guests': fields.Integer,
        'from_date': fields.String,
        'to_date': fields.String,
        'from_time': fields.String,
        'to_time': fields.String,
    }

    @staticmethod
    @marshal_with(formater)
    def rental_by_json(rental):
        return rental
