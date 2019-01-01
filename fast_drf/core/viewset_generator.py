from rest_framework import viewsets
from rest_framework.response import Response

__author__ = 'Ashraful'


class APIViewSetGenerator(object):
    permission_classes = None
    serializer_class = None
    viewset_class = None
    queryset = None
    model = None

    def __init__(self, *args, **kwargs):
        self.model = kwargs.get('model')
        self.serializer_class = kwargs.get('serializer_class', None)
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

    def make_runtime_viewset(self, **kwargs):
        """
        Viewset Maker while it's not available on model. It's a generic viewset maker for any model
        :param func_kwargs: all the extra params are accepted and pass to child
        :return: return a viewset
        """

        class RunTimeViewset(viewsets.ModelViewSet):
            if not self.permission_classes:
                permission_classes = self.permission_classes
            serializer_class = self.serializer_class
            queryset = self.queryset

            class Meta:
                _model = self.model

            def list(self, request, **kwargs):
                _queryset = self.Meta._model.objects.all()
                return Response(self.serializer_class(_queryset, many=True).data)

            def create(self, request, **kwargs):
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.data)

            def get_queryset(self, *args, **kwargs):
                return self.Meta._model.objects.all()

        return RunTimeViewset
