## Why Fast DRF?
Fast DRF(Django REST Framework) is for making REST API development quicker/faster with awesomeness of Django. It will
help you to write less code and develop API fastest as you can. Also you can override everthing(queryset, view class,
serializer, etc) you want.
### Features
1. Runtime API creation without writing View, Serializer, Url, etc
2. API versioning by default.
3. Control fields on each versions
4. An enhanced filtering support align with Django query filter.
5. Customizable API URL and API Prefix.
6. Options for Overriding Viewset, Serializer, Queryset
7. Query optimization enabled for API with Django's `prefetch_related` and `select_related`
8 Full control over project during making automated API. i.e: you can select an Django app to enable for making API.

## How it works?
It has a plain and simple architecture. It brings your configuration and create a runtime serializer and a runtime viewset. So, there is no option to slow down your API. It's similar as native rest framework.  

**Procedure of execution**  
* Locate the enabled apps from settings. If not read all the apps from installed apps.(I always recommend to keep **ENABLED_APPS** in settings)  
* Read configuration from each model.  
* Create a runtime serializer and runtime view.  
* Read REST framework configuration from settings.py and put them in viewset class. For example, You may have Custom Pagination class, Default Permission class like **IsAuthenticated** etc...  
* Bind into urls. It's has a own router and the router return urlpatterns in a list.  

## Installation
* Install from pypy  
```bash
pip install fast-drf
```

* Edit your `settings.py` and add the following lines,
```python
FAST_DRF_CONFIG = {
    'DEFAULT_APPLIED_APPS': (
        'example_app', 'another_app'
    )
}
```

* On your `urls.py`
```
from fast_drf.router import BasicRouter

urlpatterns = BasicRouter.get_urls()
```

## The minimal Configuration to expose an API.(Quick Start)
Write the following classmethod into your model. and don't forget to extend from **ExposeApiModelMixin** your model.
```python
@classmethod
def exposed_api(cls, *args, **kwargs):
    return {
        'api_url': 'an-awesome-api'
    }
```
Now you will get API like, `/api/v1/an-awesome-api/`

## Version your API

Suppose you have an API and your API using by so many client software. Now you found a bug or just need to remove some
fields or add some fields. In that case your existing clients get interrupted. So, what you will do? Keep the old API
and make a new one without extras hassle. Follow me,

```python
@classmethod
def api_version_fields(cls, **kwargs):
    return {
        'v1': ['id', 'name', 'custom_1', 'custom_2'],
        'v2': {
            'fields': ('id', 'name', 'something_else', 'field_1', 'field_2', 'field_xx'),
            'read_only_fields': ('field_1',),
            'write_only_fields': ('field_xx',),
            'optional_fields': ('field_2',)
        },
    }
```
Here, 
1. **fields** means all the fields those will be basically exposed the API.  
2. **read_only_fields** means those fields will not affect on the POST/PUT/PATCH method.  
3. **write_only_fields** means the fields will not affect the GET method  
4. **optional_fields** means it's not required on POST/PUT/PATCH  

**Note** You can pass list or tuple. But you must make sure that everthing you have passed into the each array that must
me self attribute. For example, In this case `something_else` must be a model property, fields. Remember model custom
properties are always readonly fields. You can write into model like following,

```python
@property
def something_else(self):
    return 'This is a value'
```

## Enable Trailing Slash

Set `APPEND_SLASH = True` at your settings.py

## You don't like `/api/` as a prefix

Set you API prefix as your own like following. Just update into `settings.py`

```python
FAST_DRF_CONFIG = {
    # ...
    'DEFAULT_API_PREFIX': 'rest-api'  # Default 'api'
    # ...
}
```

Your API will look like, /rest-api/v1/users/

## Full Configuration

* As you already installed the package, So, now update your every model or if you use base abstract model then it's good
  and less time you need. Update model like following,

```python
from fast_drf.mixins.expose_api_model_mixin import ExposeApiModelMixin
from django.db import models


class MyModel(ExposeApiModelMixin, models.Model):
    # ... All yor fields

    # The following methods are available from model mixin
    @classmethod
    def exposed_api(cls, *args, **kwargs):
        """
        This method holds a bunch of API configs and return like following...
        {
            "api_url": "",  # (REQUIRED)

            # You must use from HTTPVerbsEnum. Like HTTPVerbsEnum.GET.value, HTTPVerbsEnum.POST.value
            "allowed_methods": ['get', 'post', 'put', 'patch', 'delete'], # (NOT REQUIRED)

            # slug_field is application 'put', 'patch', 'delete' these methods
            "slug_field": "pk", # (NOT REQUIRED) DEFAULT [PK] (Must be model field, unique or primary key)
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

**That's it.** You can also override serializer class and viewset class

## Filtering on API

Suppose you have a nice API like: `api/v1/posts/`. I assume your model have fields like, `title`, `description`
, `author`(ForeignKey with User) etc. And you need to filter you data based on these fields. Where it comes default
filtering enabled for all the model fields. You just need to pass the param into the API just like following...

```
http://yourdomain.com/api/v1/posts/?search=1&title:icontains=test&description:icontains=hello&author_id=10
```

You don't need to pass all the fields. Just pass the param you want to be filtered out. One thing to remember
is `search=1`. If you forget to put it, you won't be able to filter using all those params. So, `search=1` is important
here. Another good news is, here it supports all the django filtering options like, `icontains`, `contains`, `exact`
, `iexact` etc. Remember whenever you are going to use one of these you must seperate the filtered field with `:`.
Like, `title:icontains`. That's it :)

## Optimizing the Number of Queries

Do you like to optimize the number of queries over the API? If YES? you are on the right place. As we are working wit
Django and DRF. We have a built in support for prefetch and select. To know more about this please
visit https://docs.djangoproject.com/en/3.1/ref/models/querysets/#select-related.  
The following implementation works for our library.

```python
class MyModel(ExposeApiModelMixin, models.Model):
    @classmethod
    def exposed_api(cls, *args, **kwargs):
        pass

    # All yor fields
    @classmethod
    def api_prefetch_related_fields(cls):
        # Only the m2m and reverse related fields
        return ['field_1', 'field_2']

    @classmethod
    def api_select_related_fields(cls):
        # Only foreignkey fields
        return ['field_1', 'field_2']
```

So, Where you have enabled the API and you have some relational fields you just need to declare them on the list to
optimize the database joining.

## Override queryset for API

The previous implementation was "queryset" on exposed_api method. But, it has some drawbacks. So, we are moving to
`get_api_queryset` method. The implementation is simple. Let's dig into this.

```python
@classmethod
def get_api_queryset(cls, request):
    """
    This method will be used for overriding the queryset for API.
    You can use the request here.
    """
    return cls.objects.filter(your_filter='data')
```
