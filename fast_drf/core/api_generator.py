from rest_framework import serializers, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from fast_drf.core.viewset_generator import APIViewSetGenerator


class APIGenerator(object):
    permission_classes = None
    serializer_class = None
    viewset_class = None
    queryset = None
    model = None

    def __init__(self, *args, **kwargs):
        self.model = kwargs.get('model')
        self.serializer_class = kwargs.get('serializer_class', self.get_runtime_serializer(**kwargs))
        self.viewset_class = kwargs.get('viewset_class')
        self.permission_classes = kwargs.get('permission_classes', [])
        self.queryset = kwargs.get('queryset', self.get_queryset(**kwargs))

    def get_queryset(self, *args, **kwargs):
        """
        Queryset maker for model
        :param args:
        :param kwargs:
        :return: a queryset
        """
        return self.model.objects.all()

    def get_runtime_viewset(self, **kwargs):
        """
        Viewset finder and return
        :param kwargs: all the extra params are accepted and pass to child
        :return: a viewset class
        """
        if self.viewset_class is None:
            return APIViewSetGenerator.make_runtime_viewset(**kwargs)
        return self.viewset_class

    def get_runtime_serializer(self, **kwargs):
        """
        Serializer finder and return
        :param kwargs: all the extra params are accepted and pass to child
        :return: return a serializer class
        """
        if self.serializer_class is None and self.model:
            return self.make_runtime_serializer(**kwargs)
        return self.serializer_class

    def make_runtime_serializer(self, **func_kwargs):
        """
        A generic serializer maker at server first run
        :param func_kwargs: all the extra params are accepted and pass to child
        :return: return serializer class
        """
        class RuntimeModelSerializer(serializers.ModelSerializer):
            class Meta:
                model = self.model
                fields = '__all__'

        return RuntimeModelSerializer
