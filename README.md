# Fast DRF [![Documentation Status](https://readthedocs.org/projects/fast-drf/badge/?version=latest)](https://fast-drf.readthedocs.io/en/latest/?badge=latest) [![Python packaging](https://github.com/iashraful/fast-drf/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/iashraful/fast-drf/actions/workflows/python-package.yml)
> Fast DRF is a small library for making API faster with Django and Django REST Framework.
It's easy and configurable.

### Full Documentation [here](https://fast-drf.readthedocs.io/en/latest/)
### Change Log is [here](https://github.com/iashraful/fast-drf/blob/master/CHANGELOG.md)

### Features
1. Runtime API creation without writing View, Serializer, Url, etc
2. API versioning by default.
3. Control fields on each versions
4. An enhanced filtering support align with Django query filter.
5. Customizable API URL and API Prefix.
6. Options for Overriding Viewset, Serializer, Queryset
7. Query optimization enabled for API with Django's `prefetch_related` and `select_related`  
8. Full control over project during making automated API. i.e: you can select an Django app to enable for making API.

### Quick Start
* Install the library inside your  virtualenv by using pip `pip install fast-drf`
* Add 'rest_framework' to `INSTALLED_APPS`
* Add fast_drf.router.BasicRouter.get_urls() to the `urlpatterns` in `urls.py`, e.g.
```python
from django.contrib import admin
from django.urls import path
from fast_drf.router import BasicRouter

urlpatterns = [
    path('admin/', admin.site.urls),
] + BasicRouter.get_urls()
```

* Add config for Fast DRF like following,
```python
FAST_DRF_CONFIG = {
    'DEFAULT_APPLIED_APPS': (
        'example_app', 'another_app'
    )
}
```
* Update your every model or if you use base abstract model then it's good and less time you need. Update model like following,
**Overriding the `expose_api` classmethod is not necessary anymore. If you just inherit the `ExposeApiModelMixin` mixin class then your app will be detect a api url accordingly.**
```python
from fast_drf.mixins.expose_api_model_mixin import ExposeApiModelMixin
from django.db import models


class MyModel(ExposeApiModelMixin, models.Model):
    #... All yor fields
    pass
    
    # The following methods are available from model mixin
    @classmethod
    def exposed_api(cls, *args, **kwargs):
        """
        This method holds a bunch of API configs and return like following...
        {
            "api_url": "",  # (NOT REQUIRED)

            # You must use from HTTPVerbsEnum. Like HTTPVerbsEnum.GET.value, HTTPVerbsEnum.POST.value
            "allowed_methods": ['get', 'post', 'put', 'patch', 'delete'], # (NOT REQUIRED)

            # slug_field is application 'put', 'patch', 'delete' these methods
            "slug_field": "pk", # (NOT REQUIRED) DEFAULT [PK] (Must be model field, unique or primary key)

            "queryset": "",  # (NOT REQUIRED) default all
            "viewset_class": "",  # (NOT REQUIRED) BaseViewset class
            "serializer_class": "",  # (NOT REQUIRED) default BaseEntitySerializer
            "permission_classes": "",  # (NOT REQUIRED) default set from settings
        }
        :param args:
        :param kwargs:
        :return: An empty Dictionary/False OR Full config dictionary.
        """
        api_configs = {
            "api_url": 'my-model-api',
        }
        return api_configs

```

#### Enable multiple API version
To achieve this awesomeness rewrite the following method in your model
```python
@classmethod
def api_version_fields(cls, **kwargs):
    """
    *** DEFAULT VERSION `v1` ***

    This method will return a dictionary object with version number and fields name. Fields are similar like
    serializer fields. Or you can say exactly as same as serializer fields.
    :param kwargs: Currently nothing to receive on kwargs
    :return: a dictionary object with version number
    """
    versions = {
        'v1': ['id', 'name', 'custom_1', 'custom_2'],
        'v2': ['id', 'name', 'something_else']
    }
    return versions
```


#### Append a slash at the end of of API
Set `APPEND_SLASH = True` at your settings.py

#### API Prefix Change
Set you API prefix as your own like following.  
```python
FAST_DRF_CONFIG = {
    # ...
    'DEFAULT_API_PREFIX': 'rest-api'  # Default 'api'
    # ...
}
```
Your API will look like, `/rest-api/v1/users/`


**That's it.** You can also override serializer class and viewset class
