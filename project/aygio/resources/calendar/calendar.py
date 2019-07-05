from datetime import datetime

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import reqparse, Resource

from project.database import db
from project.aygio.models.system import DataSystem
from project.aygio.models.calendar import Calendar, GuestInfo, Rental
from project.aygio.api_manager.getter_api import get_api_manager
from project.authorization.models import User
from project.errors.custom_exceptions import (UserNotExist,
                                              PropNotExist,
                                              InvalidaDate,
                                              FlatNotExist,
                                              ConnectionToForeignData,
                                              SysNotExist)
from project.aygio.models.flat import Flat
from project.aygio.models.property import Property


OUTER_CLIENT_ID = "NozfgeXqqJjvbAPCiURUrgaCMLDus7C9HYo2zMtP"


class CalendarInfoAPI(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('flat_id', type=int, required=True, location='json')
    post_parser.add_argument('start_date', required=True, location='json')
    post_parser.add_argument('end_date', required=True, location='json')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('flat_id', type=int, required=True, location='args')
    get_parser.add_argument('sort_type', location='args')
    get_parser.add_argument('reverse', type=str, location='args')
    get_parser.add_argument('from_date', location='args')
    get_parser.add_argument('to_date',  location='args')

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()

        if not User.query.filter_by(id=user_id).first():
            raise UserNotExist

        args = self.post_parser.parse_args()
        flat_id = args['flat_id']
        if not Flat.query.filter_by(id=flat_id).first():
            raise FlatNotExist

        props = Property.query.filter_by(flat_id=flat_id).all()
        if len(props) == 0:
            raise PropNotExist

        availabilities = []
        for prop in props:
            if not prop.local_user_id == user_id:
                raise ConnectionToForeignData

            data_sys = DataSystem.query.filter_by(user_id=user_id, system_id=prop.system_id).first()
            if not data_sys:
                raise SysNotExist

            calendars = Calendar.query.filter_by(property_id=prop.id).all()
            for calendar in calendars:
                GuestInfo.query.filter_by(calendar_id=calendar.id).delete()

            GuestInfo.query.filter_by(calendar_id=prop.id).delete()
            db.session.commit()
            Calendar.query.filter_by(property_id=prop.id, system_id=prop.system_id).delete()
            db.session.commit()

            manager = get_api_manager(prop.system_id)
            sys_avail = manager.load_calendar(data_sys.token,
                                              args['flat_id'],
                                              prop.id,
                                              prop.inner_id,
                                              args['start_date'],
                                              args['end_date'])

            availabilities += sys_avail

        for avail in availabilities:
            db.session.add(avail)
        db.session.commit()

        bookings = manager.load_accommodation(data_sys.name_slug, data_sys.token)
        db.session.commit()

        for item in bookings:
            db.session.add(item)

        db.session.commit()
        db.session.close()

        return jsonify(dict(success=True))

    @jwt_required
    def get(self):

        args = self.get_parser.parse_args()
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

        # <<>>
        calendar_info = []
        props = Property.query.filter_by(flat_id=flat_id).all()
        for prop in props:
            calendars = Calendar.query.filter_by(property_id=prop.id).all()

            for cal in calendars:
                cal_json = Calendar.calendar_by_json(cal)

                if cal.availability == 'unavailable' or cal.availability == 'nocheckout':
                    rental = Rental.query.filter_by(flat_id=flat_id,
                                                    from_date=cal.start_date,
                                                    to_date=cal.end_date).first()
                    if rental:
                        cal_json['rental'] = Rental.rental_by_json(rental)
                    else:
                        guest = GuestInfo.query.filter_by(calendar_id=cal.id).first()
                        if guest:
                            cal_json['guest'] = GuestInfo.guest_by_json(guest)

                calendar_info.append(cal_json)

        # <<< Filtered calendar data>>>
        filtred_calendar = []
        if args['from_date'] and args['to_date']:
            from_date = datetime.strptime(args['from_date'], '%Y-%m-%d')
            to_date = datetime.strptime(args['to_date'], '%Y-%m-%d')

            if from_date >= to_date:
                raise InvalidaDate

            for cal in calendars:
                cal_start_date = datetime.strptime(cal.start_date, '%Y-%m-%d')
                cal_end_date = datetime.strptime(cal.end_date, '%Y-%m-%d')

                if from_date <= cal_end_date and cal_start_date <= to_date:
                    filtred_calendar.append(dict(Calendar.calendar_by_json(cal)))

        # <<< Sorting calendar data >>>
        if args['sort_type']:
            key = Calendar.formater.keys()
            if args['sort_type'] in key:
                sort_type = args['sort_type']
            else:
                sort_type = 'start_date'
        else:
            sort_type = 'start_date'

        if args['reverse']:
            if args['reverse'].lower() == 'false':
                reverse = False
            elif args['reverse'].lower() == 'true':
                reverse = True
        else:
            reverse = False

        calendar_info = sorted(calendar_info, key=lambda k: k.get(sort_type), reverse=bool(reverse))

        return jsonify(dict(
            success=True,
            filtred_calendar=filtred_calendar,
            calendars=calendar_info
        ))

