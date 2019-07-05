from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import fields, marshal_with, Resource

from project.authorization.models import User
from project.aygio.models.flat import Flat
from project.aygio.models.property import Property
from project.aygio.models.system import DirSystem

from project.errors.custom_exceptions import (
    FlatNotExist,
    PropNotExist,
    UserNotExist
)

prop_fields = {
        'id': fields.Integer,
        'system_name': fields.String,
        'system_url_img': fields.String,
    }

flat_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'country': fields.String,
        'city': fields.String,
        'district': fields.String,
        'photo_url': fields.String,
        'count_props': fields.Integer,
        'props':  fields.List(fields.Nested(prop_fields))
    }


class GetFlat(Resource):

    @staticmethod
    def create_prop_info(prop, system_of_prop):
        return dict(
            id=prop.id,
            system_name=system_of_prop.name,
            system_url_img=system_of_prop.url_img
        )

    @staticmethod
    @marshal_with(flat_fields)
    def flat_by_json(flat, prop, count_props, json_props):

        return dict(
            id=flat.id,
            name=flat.name,
            country=prop.country,
            city=prop.city,
            district=prop.district,
            photo_url=prop.photo_url,
            count_props=count_props,
            props=json_props
            )

    @jwt_required
    def get(self):
        curr_user_id = get_jwt_identity()

        user = User.query.filter_by(id=curr_user_id).first()
        if not user:
            raise UserNotExist

        systems = DirSystem.query.all()

        flats = Flat.query.filter_by(user_id=curr_user_id).all()
        if len(flats) == 0:
            raise FlatNotExist

        props = Property.query.filter_by(local_user_id=curr_user_id).all()
        if len(props) == 0:
            raise PropNotExist

        json_flats = []
        for fl in flats:
            props_of_fl = list(filter(lambda p: p.flat_id == fl.id, props))
            count_props = len(props_of_fl)

            if count_props == 0:
                raise PropNotExist

            arr_props = []
            for prop in props_of_fl:
                arr_sys = list(filter(lambda s: prop.system_id == s.id, systems))
                prop_info = GetFlat.create_prop_info(prop, arr_sys[0])

                arr_props.append(prop_info)

            str_flat = GetFlat.flat_by_json(
                fl,
                props_of_fl[0],
                count_props,
                arr_props
                )

            json_flats.append(str_flat)

        return jsonify(dict(
            success=True,
            flats=json_flats
        ))

