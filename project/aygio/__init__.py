from flask import Blueprint
from flask_restful import Api

from project.aygio.resources.photo.gallery import Gallery
from project.aygio.resources.photo.upload_photo import UploadPhoto

from project.aygio.resources.system.add_system import AddSystem
from project.aygio.resources.system.all_systems import AllSystems
from project.aygio.resources.system.get_system import GetUserSystems

from project.aygio.resources.property.min_stay import ChangeMinStay
from project.aygio.resources.property.num_guests import ChangeNumGuests
from project.aygio.resources.property.properties import Properties
from project.aygio.resources.property.refresh import Refresh

from project.aygio.resources.flat.add_to_flat import AddToFlat
from project.aygio.resources.flat.get_flat import GetFlat
from project.aygio.resources.flat.join_flat import JoinFlat
from project.aygio.resources.flat.delete_from_flat import DeleteFromFlat
from project.aygio.resources.flat.flat_name import ChangeFlatName

from project.aygio.resources.calendar.calendar import CalendarInfoAPI
from project.aygio.resources.calendar.add_rental import AddRental


bp = Blueprint('aygio', __name__)
api = Api(bp)


api.add_resource(Gallery, '/api/gallery')
api.add_resource(UploadPhoto, '/api/uploadphoto')

api.add_resource(AddSystem, '/api/add_system')
api.add_resource(AllSystems, '/api/allsystems')
api.add_resource(GetUserSystems, '/api/mysystems')

api.add_resource(ChangeMinStay, '/api/minstay')
api.add_resource(ChangeNumGuests, '/api/numguests')
api.add_resource(Properties, '/api/properties')
api.add_resource(Refresh, '/api/refresh')

api.add_resource(AddToFlat, '/api/addtoflat')
api.add_resource(DeleteFromFlat, '/api/deletefromflat')
api.add_resource(GetFlat, '/api/myflats')
api.add_resource(JoinFlat, '/api/joinflat')
api.add_resource(ChangeFlatName, '/api/flatname')

api.add_resource(AddRental, '/api/add_rental')
api.add_resource(CalendarInfoAPI, '/api/calendar')
