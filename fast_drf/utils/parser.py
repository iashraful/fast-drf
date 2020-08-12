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
