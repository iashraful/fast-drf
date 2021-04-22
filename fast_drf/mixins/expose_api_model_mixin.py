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
            "api_url": "",  # (REQUIRED)

            # You must use from HTTPVerbsEnum. Like HTTPVerbsEnum.GET.value, HTTPVerbsEnum.POST.value
            "allowed_methods": ['get', 'post', 'put', 'patch', 'delete'], # (NOT REQUIRED)

            # slug_field is application 'put', 'patch', 'delete' these methods
            "slug_field": "pk", # (NOT REQUIRED) DEFAULT [PK] (Must be model field, unique or primary key)
            # This "queryset" is deprecated. Will be removed in future versions. Instead on this use the model's
            # get_api_queryset method
            "queryset": "",  # (NOT REQUIRED) default all
            "viewset_class": "",  # (NOT REQUIRED) BaseViewset class
            "serializer_class": "",  # (NOT REQUIRED) default BaseEntitySerializer
            "permission_classes": "",  # (NOT REQUIRED) default set from settings
        }
        :param args:
        :param kwargs:
        :return: An empty Dictionary/False OR Full config dictionary.
        """
        api_configs = {}
        return api_configs

    @classmethod
    def api_version_fields(cls, **kwargs):
        """
        *** DEFAULT VERSION `v1` ***

        This method will return a dictionary object with version number and fields name. Fields are similar like
        serializer fields. Or you can say exactly as same as serializer fields.
        :param kwargs: Currently nothing to receive on kwargs
        :return: a dictionary object with version number
        """
        versions = {}
        return versions

    @classmethod
    def api_prefetch_related_fields(cls):
        """
        Prefetch related is used for prefeching the objects for Django Queryset. It saves a lot time
        of table joining and multiple queries.
        Read more: https://docs.djangoproject.com/en/3.1/ref/models/querysets/#prefetch-related

        Return a lists of field name those will be directly using on the queryset.
        """
        return []

    @classmethod
    def api_select_related_fields(cls):

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
