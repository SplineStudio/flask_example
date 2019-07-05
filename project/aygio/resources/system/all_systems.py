from flask import jsonify
from flask_restful import fields, marshal_with, Resource
from project.aygio.models.system import DirSystem
from project.errors.custom_exceptions import SysNotExist


class AllSystems(Resource):
    property_fields = {
        'system_id': fields.String,
        'name': fields.String,
        'url_img': fields.String,
    }

    @staticmethod
    @marshal_with(property_fields)
    def sys_by_json(sys):
        return dict(
            system_id=sys.id,
            name=sys.name,
            url_img=sys.url_img
        )

    def get(self):

        all_sys = DirSystem.query.all()
        if len(all_sys) == 0:
            raise SysNotExist

        json_props = []
        for sys in all_sys:
            json_props.append(AllSystems.sys_by_json(sys))

        return jsonify(dict(
            success=True,
            systems=json_props
        ))

