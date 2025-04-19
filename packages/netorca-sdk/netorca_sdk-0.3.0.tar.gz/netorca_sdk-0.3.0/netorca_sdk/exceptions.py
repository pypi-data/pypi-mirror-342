import sys

sys.tracebacklimit = 0


class NetorcaBaseException(Exception):
    pass


class NetorcaException(NetorcaBaseException):
    pass


class NetOrcaWrongYAMLFormat(NetorcaBaseException):
    pass


class NetorcaValueError(NetorcaBaseException):
    pass


class NetorcaNotFoundError(NetorcaBaseException):
    pass


class NetorcaPermissionError(NetorcaBaseException):
    pass


class NetorcaTimeoutError(NetorcaBaseException):
    pass


class NetorcaAPIError(NetorcaBaseException):
    pass


class NetorcaAuthenticationError(NetorcaAPIError):
    pass


class NetorcaServerUnavailableError(NetorcaAPIError):
    pass


class NetorcaGatewayError(NetorcaAPIError):
    pass


class NetorcaInvalidContextError(NetorcaAPIError):
    pass
