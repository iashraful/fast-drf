from rest_framework import serializers, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from fast_drf.core.serializer_generator import SerializerGenerator
from fast_drf.core.viewset_generator import APIViewSetGenerator


class APIGenerator(object):
    def __init__(self, *args, **kwargs):
        self.api_view = APIViewSetGenerator(**kwargs)
        self.serializer = SerializerGenerator(**kwargs)

    def get_runtime_viewset(self, **kwargs):
        """
        Viewset finder and return
        :param kwargs: all the extra params are accepted and pass to child
        :return: a viewset class
        """
        # If not serializer is present
        if not self.api_view.serializer_class or (
                self.api_view.viewset_class and not self.api_view.viewset_class.serializer_class):
            _serializer_class = self.get_runtime_serializer(**kwargs)
            self.api_view.serializer_class = _serializer_class
            if self.api_view.viewset_class:
                self.api_view.viewset_class.serializer_class = _serializer_class
            # Now serializer is available
        if self.api_view.viewset_class is None:
            return self.api_view.make_runtime_viewset(**kwargs)
        return self.api_view.viewset_class

    def get_runtime_serializer(self, **kwargs):
        """
        Serializer finder and return
        :param kwargs: all the extra params are accepted and pass to child
        :return: return a serializer class
        """
        if self.api_view.serializer_class is None and self.api_view.model:
            return self.serializer.make_runtime_serializer(**kwargs)
        return self.api_view.serializer_class
