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
            "version": "",  # (NOT REQUIRED) EX: 'v1', 'v2' default 'v1'
            "queryset": "",  # (NOT REQUIRED) default all
            "api_viewset_class": "",  # (NOT REQUIRED) BaseViewset class
            "serializer_class": "",  # (NOT REQUIRED) default BaseEntitySerializer
            "permission_classes": "",  # (NOT REQUIRED) default set from settings
        }
        :param args:
        :param kwargs:
        :return: An empty Dictionary/False OR Full config dictionary.
        """
        api_configs = {}
        return api_configs
