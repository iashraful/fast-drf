from rest_framework.generics import ListCreateAPIView
from rest_framework import serializers


class ExposeApiViewsetMixin(object):
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
        self.queryset = kwargs.get('queryset', [])

    def get_runtime_viewset(self, **kwargs):
        if self.viewset_class is None:
            return self.make_runtime_viewset(**kwargs)
        return self.viewset_class

    def make_runtime_viewset(self, **func_kwargs):
        class RunTimeViewset(ListCreateAPIView):
            if self.permission_classes:
                permission_classes = self.permission_classes
            serializer_class = self.serializer_class
            queryset = self.queryset

            def get(self, request, *args, **kwargs):
                return super(RunTimeViewset, self).get(request, *args, **kwargs)

        return RunTimeViewset

    def get_runtime_serializer(self, **kwargs):
        if self.serializer_class is None and self.model:
            return self.make_runtime_serializer(**kwargs)
        return self.serializer_class

    def make_runtime_serializer(self, **func_kwargs):
        class RuntimeModelSerializer(serializers.ModelSerializer):
            class Meta:
                model = self.model
                fields = '__all__'

        return RuntimeModelSerializer
