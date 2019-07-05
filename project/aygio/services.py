from project.database import db
from project.aygio.api_manager.getter_api import get_api_manager

from project.aygio.models.photo import Photo
from project.aygio.models.property import Property
from project.aygio.models.system import DataSystem
from project.errors.custom_exceptions import FailurePropsSystem, SysNotExist


def load_all_photos(user_id):
    list_systems = DataSystem.query.filter_by(user_id=user_id).all()
    if len(list_systems) == 0:
        raise SysNotExist

    counter = 0
    for sys in list_systems:
        manager_api = get_api_manager(sys.system_id)
        photos_sys = manager_api.all_photos(sys.token)

        for photo in photos_sys:
            if not Photo.query.filter_by(property_id=photo.property_id, file_name=photo.file_name).first():
                db.session.add(photo)
                counter += 1

    if not counter == 0:
        db.session.commit()
        db.session.close()


def load_all_props(user_id, list_systems):
    properties = []
    for sys in list_systems:
        manager = get_api_manager(sys.system_id)
        prop_sys = manager.all_props(user_id, sys.token)

        if len(prop_sys) != 0:
            properties += prop_sys

    return properties


def prop_update(old_prop, fresh_prop):
    resp = {}

    for key, value in old_prop.__dict__.items():

        if key in ['_sa_instance_state', 'id', 'local_user_id', 'flat_id']:
            continue

        new_value = getattr(fresh_prop, key)
        if value != new_value:
            resp[key] = new_value
    return resp


def refresh_by_user_id(user_id):

    list_systems = DataSystem.query.filter_by(user_id=user_id).all()
    if len(list_systems) == 0:
        raise SysNotExist

    properties = load_all_props(user_id, list_systems)

    if len(properties) == 0:
        raise FailurePropsSystem

    for prop in properties:
        concurrence = Property.query.filter_by(inner_id=prop.inner_id).first()
        if concurrence:
            prop = prop_update(concurrence, prop)
            Property.query.filter_by(id=concurrence.id).update(prop)
            db.session.commit()
        else:
            db.session.add(prop)

    db.session.commit()
    db.session.close()

    load_all_photos(user_id)
