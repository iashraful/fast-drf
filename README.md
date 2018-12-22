## Fast DRF(Django REST Framework)
> Fast DRF is a small library for making API faster with Django and Django REST Framework.
It's easy and configurable.


### Quick Start
* Install the library inside your  virtualenv by using pip `pip install fast-drf`
* Update your every model or if you use base abstract model then it's good and less time you need. Update model like following,
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
            "api_url": "",  # (REQUIRED)
            "version": "",  # (COMING SOON)(NOT REQUIRED) EX: 'v1', 'v2' default 'v1'
            "queryset": "",  # (NOT REQUIRED) default all
            "api_viewset_class": "",  # (NOT REQUIRED) BaseViewset class
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

**That's it.** You can also override serializer class and viewset class