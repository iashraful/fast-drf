from copy import deepcopy


def get_default_config():
    """
    Here will be landed all the default config.
    """
    from django.conf import settings

    return {
        'DEFAULT_APPLIED_APPS': settings.INSTALLED_APPS,
        'DEFAULT_API_PREFIX': 'api',
    }


def get_config():
    """
    A little business logic is applied here. It'll always apply the user config with default config
    """
    from django.conf import settings
    _settings_key = 'FAST_DRF_CONFIG'
    default_config = get_default_config()

    if hasattr(settings, _settings_key):
        _config = getattr(settings, _settings_key, {})
        default_config.update(_config)
    return default_config


def parse_filters(model, request, **kwargs):
    from django.db.models import Q
    """
    model: The Django model,
    request: The request where user asked for the data
    """
    _fields = [f.name for f in model._meta.get_fields()]
    _params = request.GET
    _filters = {}
    for param, val in _params.items():
        try:
            if ':' in param:
                _field_name, _filter_option = param.split(':')
                if _field_name not in _fields:
                    continue
                _temp = deepcopy(param)
                _filters['{}__{}'.format(_field_name, _filter_option)] = val
            else:
                if param not in _fields:
                    continue
                _filters[param] = val
        except Exception as error:
            continue
    return Q(**_filters)


