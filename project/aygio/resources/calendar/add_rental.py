from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, Resource

from project.authorization.models import User
from project.aygio.models.flat import Flat
from project.aygio.models.property import Property
from project.database import db
from project.aygio.api_manager.getter_api import get_api_manager
from project.aygio.models.system import DataSystem
from project.aygio.models.calendar import Rental
from project.errors.custom_exceptions import (UserNotExist,
                                              FlatNotExist,
                                              ConnectionToForeignData,
                                              PropNotExist,
                                              SysNotExist)


class AddRental(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('flat_id', required=True, location='json')
    parser.add_argument('user_name', required=True, location='json')
    parser.add_argument('phone_number', required=True, location='json')
    parser.add_argument('guests', required=True, location='json')
    parser.add_argument('from_date', required=True, location='json')
    parser.add_argument('to_date', required=True, location='json')
    parser.add_argument('from_time', location='json')
    parser.add_argument('to_time', location='json')

    @jwt_required
    def post(self):
        args = self.parser.parse_args()
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()

        if not user:
            raise UserNotExist

        flat_id = args['flat_id']
        flat = Flat.query.filter_by(id=flat_id).first()

        if not flat:
            raise FlatNotExist
        if not flat.user_id == user_id:
            raise ConnectionToForeignData

        props = Property.query.filter_by(flat_id=flat_id).all()
        if len(props) == 0:
            raise PropNotExist

        for prop in props:
            manager = get_api_manager(prop.system_id)

            data_sys = DataSystem.query.filter_by(system_id=prop.system_id, user_id=user_id).first()
            if not data_sys:
                raise SysNotExist

            manager.set_unavailable(place_id=prop.inner_id,
                                    token=data_sys.token,
                                    start_date=args['from_date'],
                                    end_date=args['to_date'])

            rental = Rental(
                flat_id=args['flat_id'],
                user_name=args['user_name'],
                phone_number=args['phone_number'],
                guests=args['guests'],
                from_date=args['from_date'],
                to_date=args['to_date'],
                from_time=args['from_time'],
                to_time=args['to_time']
            )

            db.session.add(rental)

        db.session.commit()
        db.session.close()

        return jsonify(dict(success=True))
