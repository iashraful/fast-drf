from rest_framework import viewsets
from rest_framework.response import Response

__author__ = 'Ashraful'


class APIViewSetGenerator(object):
    permission_classes = None
    serializer_class = None
    viewset_class = None
    queryset = None
    model = None

    def __init__(self, *args, **main_kwargs):
        self.model = main_kwargs.get('model')
        self.serializer_class = main_kwargs.get('serializer_class', None)
        self.viewset_class = main_kwargs.get('viewset_class')
        self.permission_classes = main_kwargs.get('permission_classes', [])
        self.queryset = main_kwargs.get('queryset', self.get_queryset(**main_kwargs))
        self.lookup_field = main_kwargs.get('slug_field', 'pk')

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
            model = self.model
            lookup_field = self.lookup_field

            def list(self, request, **kwargs):
                # Here it's performing sub query in SQL. So, no performance loss. Just executing a big query
                # not more than 1 query
                _queryset = self.model.objects.filter(pk__in=self.queryset)
                return Response(self.serializer_class(_queryset, many=True).data)

            def create(self, request, *args, **kwargs):
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.data)

            def retrieve(self, request, *args, **kwargs):
                return super(RunTimeViewset, self).retrieve(request, *args, **kwargs)

            def update(self, request, *args, **kwargs):
                return super(RunTimeViewset, self).update(request, *args, **kwargs)

            def get_queryset(self, *args, **kwargs):
                return self.model.objects.all()

        return RunTimeViewset