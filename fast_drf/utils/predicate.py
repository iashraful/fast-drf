import inspect

__author__ = 'Ashraful'


def is_model(value=None):
    """
    Check a python object is a model or not. Got idea from inspect
    :param value: an object. may be function, class or anything
    :return: boolean status based on condition
    """
    if value is None:
        return False
    if inspect.isclass(value):
        try:
            _obj = value()
            if hasattr(_obj, 'pk'):
                return True
        except Exception:
            return False
    return False
