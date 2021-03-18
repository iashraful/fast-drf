from fast_drf.core.serializer_generator import SerializerGenerator
from fast_drf.core.viewset_generator import APIViewSetGenerator


class APIGenerator(object):
    def __init__(self, *args, **kwargs):
        self.api_view = APIViewSetGenerator(**kwargs)
        self.serializer = SerializerGenerator(**kwargs)

    def get_runtime_viewset(self, api_version=None, **kwargs):
        """
        Viewset finder and return
        :param kwargs: all the extra params are accepted and pass to child
        :param api_version: API version string or no
        :return: a viewset class
        """
        # If not serializer is present
        if not self.api_view.serializer_class or (
                self.api_view.viewset_class and not self.api_view.viewset_class.serializer_class) or (
                self.api_view.serializer_class and (
                hasattr(self.api_view.serializer_class, 'get_api_version')
                and self.api_view.serializer_class.get_api_version() != api_version)):
            _serializer_class = self.get_runtime_serializer(api_version=api_version, **kwargs)
            self.api_view.serializer_class = _serializer_class
            if self.api_view.viewset_class:
                self.api_view.viewset_class.serializer_class = _serializer_class
            # Now serializer is available
        if self.api_view.viewset_class is None:
            return self.api_view.make_runtime_viewset(**kwargs)
        return self.api_view.viewset_class

    def get_runtime_serializer(self, api_version=None, **kwargs):
        """
        Serializer finder and return
        :param kwargs: all the extra params are accepted and pass to child
        :param api_version: API Version string or number
        :return: return a serializer class
        """
        if (self.api_view.serializer_class is None and self.api_view.model) or (
                self.api_view.serializer_class and (
                hasattr(self.api_view.serializer_class, 'get_api_version')
                and self.api_view.serializer_class.get_api_version() != api_version)):
            return self.serializer.make_runtime_serializer(api_version=api_version, **kwargs)
        return self.api_view.serializer_class
