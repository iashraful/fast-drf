import inspect

__author__ = 'Ashraful'


def is_model(value=None):
    from django.db import models
    """
    Check a python object is a model or not. Got idea from inspect
    :param value: an object. may be function, class or anything
    :return: boolean status based on condition
    """
    if value is None:
        return False
    return inspect.isclass(value) and issubclass(value, models.Model)
