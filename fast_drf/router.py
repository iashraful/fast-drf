import inspect
from importlib import import_module

from django.conf import settings
from django.urls import path

from fast_drf.core.api_generator import APIGenerator
from fast_drf.utils import predicate
from fast_drf.utils.enums import HTTPVerbsEnum
from fast_drf.utils.parser import get_config


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
        _config = get_config()
        apps = _config.get('DEFAULT_APPLIED_APPS', [])
        for app in apps:
            try:
                _model_tuple = inspect.getmembers(import_module("{0}.{1}".format(app, 'models')), predicate.is_model)
                for model_name, model in _model_tuple:
                    _model_api_config = model.exposed_api() if hasattr(model, 'exposed_api') else {}
                    if not _model_api_config:
                        continue
                    # Updating model into exposed_api returned value/dict
                    _model_api_config.update({'model': model})
                    expose_api_object = APIGenerator(**_model_api_config)
                    # Get API Version information
                    api_versions = model.api_version_fields() if hasattr(model, 'api_version_fields') else {}
                    if len(api_versions.keys()) > 0:
                        for version in api_versions.keys():
                            _viewset_class = expose_api_object.get_runtime_viewset(api_version=version,
                                                                                   **_model_api_config)
                            _urls += [
                                path(
                                    str(cls.get_url_string(value=_model_api_config['api_url'], version=version)),
                                    cls.get_viewset_class_view(view_class=_viewset_class, api_config=_model_api_config),
                                    name=str(_model_api_config['api_url'])
                                )
                            ]
                    else:
                        _viewset_class = expose_api_object.get_runtime_viewset(**_model_api_config)
                        _urls += [
                            path(
                                str(cls.get_url_string(_model_api_config['api_url'], version='v1')),
                                cls.get_viewset_class_view(view_class=_viewset_class, api_config=_model_api_config),
                                name=str(_model_api_config['api_url'])
                            )
                        ]
                    if any([
                        HTTPVerbsEnum.PUT.value in _model_api_config.get('allowed_methods', []),
                        HTTPVerbsEnum.PATCH.value in _model_api_config.get('allowed_methods', []),
                        HTTPVerbsEnum.DELETE.value in _model_api_config.get('allowed_methods', []),
                    ]):
                        if len(api_versions.keys()) > 0:
                            for version in api_versions.keys():
                                _viewset_class = expose_api_object.get_runtime_viewset(api_version=version,
                                                                                       **_model_api_config)
                                _urls += [path(
                                    str(cls.get_url_string(_model_api_config['api_url'],
                                                           version=version)) + '<str:{0}>/'.format(
                                        _model_api_config.get('slug_field', 'pk')),
                                    cls.get_viewset_class_view(view_class=_viewset_class,
                                                               api_config=_model_api_config, details=True),
                                    name=str(_model_api_config['api_url']) + '_details'
                                )]
                        else:
                            _viewset_class = expose_api_object.get_runtime_viewset(**_model_api_config)
                            _urls += [path(
                                str(cls.get_url_string(_model_api_config['api_url'],
                                                       version='v1')) + '<str:{0}>/'.format(
                                    _model_api_config.get('slug_field', 'pk')),
                                cls.get_viewset_class_view(view_class=_viewset_class,
                                                           api_config=_model_api_config, details=True),
                                name=str(_model_api_config['api_url']) + '_details'
                            )]
            except (ModuleNotFoundError,) as error:
                continue
        return _urls

    @classmethod
    def get_url_string(cls, value, version=None):
        _config = get_config()
        if settings.APPEND_SLASH:
            value = "{0}/".format(value)
        if version:
            value = "{prefix}/{version}/{value}".format(
                prefix=_config.get('DEFAULT_API_PREFIX', 'api'), version=version, value=value)
        return value

    @classmethod
    def get_viewset_class_view(cls, view_class, api_config, **kwargs):
        try:
            _allowed_methods = api_config.get('allowed_methods', ['get'])
            actions_dict = {}
            # Default get method from parent function
            details_api = kwargs.get('details', False)
            if details_api:
                actions_dict.update(get='retrieve')
                if HTTPVerbsEnum.PUT.value in _allowed_methods:
                    actions_dict.update(put='update')
                if HTTPVerbsEnum.PATCH.value in _allowed_methods:
                    actions_dict.update(patch='partial_update')
                if HTTPVerbsEnum.DELETE.value in _allowed_methods:
                    actions_dict.update(delete='destroy')
            else:
                actions_dict.update(get='list')
                if HTTPVerbsEnum.POST.value in _allowed_methods:
                    actions_dict.update(post='create')

            return view_class.as_view(actions_dict)
        except Exception:
            return view_class.as_view()
