class UunIotException(Exception):
    """Base UunIotException class"""


class UuAppClientException(UunIotException):
    """Internal error in request pre-processing occured."""


class TokenError(UuAppClientException):
    """Error when getting/validating a token occured."""


class TokenCommandError(TokenError):
    """Server error when getting a token occured."""


class EventException(UunIotException):
    """Exception in event management system."""


class UnsupportedEvent(EventException):
    """Unknown gateway event."""


class InvalidModuleId(UunIotException):
    """Module ids can be only strings."""


class EventCannotRegisterHandler(EventException):
    """An error occured while registering a new handler for event."""


# old:
class EventRegisterAlreadyInstantiated(EventException):
    pass


class EventRegisterNotYetInstantiated(EventException):
    pass
