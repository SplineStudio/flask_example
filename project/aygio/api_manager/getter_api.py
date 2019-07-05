from project.errors.custom_exceptions import FailureSysManager
from project.aygio.api_manager.manager_9flats import Manager9Flats


def get_api_manager(sys_id):
    if sys_id == 1:
        return Manager9Flats()
    else:
        raise FailureSysManager
