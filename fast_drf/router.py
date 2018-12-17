import inspect
from django.conf import settings
from django.urls import path
from importlib import import_module

from fast_drf.mixins.expose_api_viewset_mixin import ExposeApiViewsetMixin


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
                    expose_api_object = ExposeApiViewsetMixin(**_model_api_config)
                    _viewset_class = expose_api_object.get_runtime_viewset(**_model_api_config)
                    _urls += [path(str(_model_api_config['api_url']), _viewset_class.as_view(),
                                   name=str(_model_api_config['api_url']))]
            except ModuleNotFoundError:
                continue
        return _urls
