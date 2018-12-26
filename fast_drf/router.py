import inspect
from importlib import import_module

from django.conf import settings
from django.urls import path

from fast_drf.core.api_generator import APIGenerator
from fast_drf.utils import predicate


class BasicRouter(object):
    """
    BasicRouter is for making basic urls for django app.
    """
    @classmethod
    def get_urls(cls, **kwargs):
        """
        Making Django Url here.
        :param kwargs:
        :return: a tuple of list [(model_name, model), (model_name, model)]
        """
        _urls = []
        apps = getattr(settings, 'FAST_API_ENABLED_APPS') if hasattr(
            settings, 'FAST_API_ENABLED_APPS') else settings.INSTALLED_APPS
        for app in apps:
            try:
                _model_tuple = inspect.getmembers(import_module("{0}.{1}".format(app, 'models')), predicate.is_model)
                for model_name, model in _model_tuple:
                    _model_api_config = model.exposed_api() if hasattr(model, 'exposed_api') else {}
                    if not _model_api_config:
                        continue
                    _model_api_config.update({'model': model})
                    expose_api_object = APIGenerator(**_model_api_config)
                    _viewset_class = expose_api_object.get_runtime_viewset(**_model_api_config)
                    _urls += [path(str(cls.get_url_string(_model_api_config['api_url'])), _viewset_class.as_view(),
                                   name=str(_model_api_config['api_url']))]
            except ModuleNotFoundError:
                continue
        return _urls

    @classmethod
    def get_url_string(cls, value):
        if settings.APPEND_SLASH:
            return "{0}/".format(value)
        return value
