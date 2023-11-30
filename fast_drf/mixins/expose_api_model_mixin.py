from typing import List, Union, Optional, Dict, Type

from rest_framework.permissions import BasePermission


class ExposeApiModelMixin(object):
    """
    ==== MODEL MIXIN ====

    This Mixin(Class) will help to generate automatic api from models with few configs
    """

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
            "viewset_class": "",  # (NOT REQUIRED) BaseViewset class
            "serializer_class": "",  # (NOT REQUIRED) default BaseEntitySerializer
            "permission_classes": "",  # (NOT REQUIRED) default set from settings
        }
        :param args:
        :param kwargs:
        :return: An empty Dictionary/False OR Full config dictionary.
        """
        api_configs = {
            "api_url": "{app_label}-{model_name}s".format(
                app_label=cls._meta.app_label, model_name=cls.__name__.lower()
            )
        }
        return api_configs

    @classmethod
    def api_version_fields(cls, **kwargs) -> dict:
        """
        *** DEFAULT VERSION `v1` ***

        This method will return a dictionary object with version number and fields name. Fields are similar like
        serializer fields. Or you can say exactly as same as serializer fields.
        :param kwargs: Currently nothing to receive on kwargs
        :return: a dictionary object with version number
        The dictionary format should be like following...
        Ex-1: { 'v1': ('field_1', 'field_2',), 'v2': ('field_1', 'field_2', 'field_3',) }
        Ex-2: {
                'v1': {
                    'fields': ('field_1', 'field_2',),
                    'read_only_fields': ('field_1',),
                    'write_only_fields': ('field_xx',),
                    'optional_fields': ('field_2',)
                },
                'v2': ('field_1', 'field_2', 'field_3',)
            }
        *Note:*
            1. "read_only_fields" means those fields will not affect on the POST/PUT/PATCH method.
            2. "write_only_fields" means the fields will not affect the GET method
            3. "optional_fields" means it's not required on POST/PUT/PATCH
            4. "fields" means all the fields those will be basically exposed the API.
        """
        versions = {}
        return versions

    def _get_version_names(self):
        pass

    @classmethod
    def api_prefetch_related_fields(cls) -> List[str]:
        """
        Prefetch related is used for prefeching the objects for Django Queryset. It saves a lot time
        of table joining and multiple queries.
        Read more: https://docs.djangoproject.com/en/3.1/ref/models/querysets/#prefetch-related

        Return a lists of field name those will be directly using on the queryset.
        """
        return []

    @classmethod
    def api_select_related_fields(cls) -> List[str]:
        """
        Select related is used for prefeching the objects for Django Queryset. It saves a lot time
        of table joining and multiple queries.
        Read more: https://docs.djangoproject.com/en/3.1/ref/models/querysets/#select-related

        Return a lists of field name those will be directly using on the queryset.
        """
        return []

    @classmethod
    def get_api_queryset(cls, *args, **kwargs):
        """
        This method will be used for overriding the queryset for API.
        """
        return cls.objects.all()

    @classmethod
    def get_api_permissions(
        cls, **kwargs
    ) -> Dict[str, Union[List[Type[BasePermission]]]]:
        """
        Return a List of permission classes. Also,
        None Just means DEFAULT FROM SETTINGS
        {
            "list": [Permission Classes,],
            "retrieve": [Permission Classes,],
            "create": [Permission Classes,],
            "update": [Permission Classes,],
            "destroy": [Permission Classes,],
            "partial_update": [Permission Classes,],
        }
        """

        return None
