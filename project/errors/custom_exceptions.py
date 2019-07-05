class DefaultException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

# Errors in request body
# Not exist exception's


class FlatNotExist(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Flat not exist")


class PhotoNotExist(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Photo not exist")


class PropNotExist(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Property not exist")


class SysNotExist(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "System not exist")


class UserExist(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "User with this data already exists")


class UserNotExist(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "User not exist")


class EmptyListOnRequest(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "List in request body are empty")

#wrong value in request


class FailureCheckObj(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Invalid request body")


class FailurePropsSystem(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Are not any properties in systems")


class FailureSysManager(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Support of system not implemented")


class FlatWithoutProperty(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Attempt get property from non-connected flat")


class OutDate(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, 'The code is out of date', 401)

#Security error's


class ConnectionToForeignData(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Attempt connection to foreign data", 403)


class ConnectionOccupiedProperty(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Attempt connect flat to occupied property", 403)


class ForeignProperty(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Property connect with other flat", 403)


class ImpossibleSystemCommand(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Attempt call non security command", 403)


class ReconnectSystem(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Attempt reconnect to system", 403)


class WrongCodeRecovery(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Wrong code recovery", 401)


class WrongPassword(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Wrong password", 401)

#System's error's


class UnavailableProp(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, 'Property have connected with flat', 403)


class OutSystemConnect(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Error connecting the system", 421)


class OldData(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Please refresh app data", 426)


class InvalidaDate(DefaultException):

    def __init__(self):
        DefaultException.__init__(self, "Invalid date", 422)

