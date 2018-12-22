import inspect
from django.conf import settings
from django.urls import path
from importlib import import_module

from fast_drf.core.api_generator import APIGenerator


class BasicRouter(object):
    @classmethod
    def get_urls(cls, **kwargs):
        _urls = []
        apps = settings.INSTALLED_APPS
        for app in apps:
            try:
                _model_tuple = inspect.getmembers(import_module("{0}.{1}".format(app, 'models')), inspect.isclass)
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
