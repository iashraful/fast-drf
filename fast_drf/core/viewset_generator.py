from rest_framework import viewsets
from rest_framework.response import Response

from fast_drf.utils.parser import parse_filters

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
        self.lookup_field = main_kwargs.get('slug_field', 'pk')

    def make_runtime_viewset(self, **kwargs):
        """
        Viewset Maker while it's not available on model. It's a generic viewset maker for any model
        :param func_kwargs: all the extra params are accepted and pass to child
        :return: return a viewset
        """

        class RunTimeViewset(viewsets.ModelViewSet):
            if self.permission_classes:
                permission_classes = self.permission_classes
            serializer_class = self.serializer_class
            model = self.model
            lookup_field = self.lookup_field

            def get_queryset(self, *args, **kwargs):
                _prefetch_related_fields = self.model.api_prefetch_related_fields()
                _select_related_fields = self.model.api_select_related_fields()
                queryset = self.model.get_api_queryset(*args, **kwargs)
                if len(_prefetch_related_fields) > 0:
                    queryset = queryset.prefetch_related(*_prefetch_related_fields)
                if len(_select_related_fields) > 0:
                    queryset = queryset.select_related(*_select_related_fields)
                return queryset

            def list(self, request, **kwargs):
                base_queryset = self.get_queryset(request=request, **kwargs)
                request = kwargs.get('request', self.request)
                try:
                    search_enabled = bool(eval(request.GET.get('search', '0')))
                    if search_enabled:
                        _filters = parse_filters(model=self.model, request=request)
                        self.queryset = base_queryset.filter(_filters)
                except Exception as err:
                    self.queryset = base_queryset
                page = self.paginate_queryset(base_queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(base_queryset, many=True)
                return Response(serializer.data)

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

            def partial_update(self, request, pk=None, *args, **kwargs):
                return super(RunTimeViewset, self).partial_update(request=request, pk=pk, *args, **kwargs)

            def destroy(self, request, pk=None, *args, **kwargs):
                return super(RunTimeViewset, self).destroy(request=request, pk=pk, *args, **kwargs)

        return RunTimeViewset
