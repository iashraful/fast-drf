import enum

__author__ = 'Ashraful'


class BaseEnum(enum.Enum):
    pass


class HTTPVerbsEnum(BaseEnum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'
