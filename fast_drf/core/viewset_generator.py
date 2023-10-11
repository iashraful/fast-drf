from rest_framework import viewsets
from rest_framework.response import Response
from fast_drf.core.class_factory import class_factory

from fast_drf.signals import *
from fast_drf.utils.parser import parse_filters

__author__ = "Ashraful"


class APIViewSetGenerator(object):
    permission_classes = None
    serializer_class = None
    viewset_class = None
    queryset = None
    model = None

    def __init__(self, *args, **main_kwargs):
        self.model = main_kwargs.get("model")
        self.serializer_class = main_kwargs.get("serializer_class", None)
        self.viewset_class = main_kwargs.get("viewset_class")
        self.permission_classes = main_kwargs.get("permission_classes", [])
        self.lookup_field = main_kwargs.get("slug_field", "pk")

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

            def get_permissions(self, **kwargs):
                _permissions = self.model.get_api_permissions(**kwargs)
                if isinstance(_permissions, list):
                    self.permission_classes = _permissions
                if isinstance(_permissions, dict):
                    if self.action in _permissions.keys():
                        self.permission_classes = _permissions[self.action]
                return super(RunTimeViewset, self).get_permissions(**kwargs)

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
                self.queryset = self.get_queryset(request=request, **kwargs)
                request = kwargs.get("request", self.request)
                try:
                    search_enabled = bool(eval(request.GET.get("search", "0")))
                    if search_enabled:
                        _filters = parse_filters(model=self.model, request=request)
                        self.queryset = self.queryset.filter(_filters)
                except Exception as err:
                    self.queryset = self.queryset
                page = self.paginate_queryset(self.queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(self.queryset, many=True)
                return Response(serializer.data)

            def create(self, request, *args, **kwargs):
                before_post_api.send(sender=self.model, requested_data=request.data)
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    instance = serializer.save()
                    after_post_api.send(
                        sender=self.model,
                        instance=instance,
                        requested_data=request.data,
                    )
                    return Response(serializer.data)
                return Response(serializer.data)

            def retrieve(self, request, *args, **kwargs):
                return super(RunTimeViewset, self).retrieve(request, *args, **kwargs)

            def update(self, request, *args, **kwargs):
                instance = self.get_object()
                before_put_api.send(
                    sender=self.model, instance=instance, requested_data=request.data
                )
                serializer = self.serializer_class(data=request.data, instance=instance)
                if serializer.is_valid(raise_exception=True):
                    instance = serializer.save()
                    after_put_api.send(
                        sender=self.model,
                        instance=instance,
                        requested_data=request.data,
                    )
                    return Response(serializer.data)
                return Response(serializer.data)

            def partial_update(self, request, *args, **kwargs):
                instance = self.get_object()
                before_patch_api.send(
                    sender=self.model, instance=instance, requested_data=request.data
                )
                serializer = self.serializer_class(
                    data=request.data, instance=instance, partial=True
                )
                if serializer.is_valid(raise_exception=True):
                    instance = serializer.save()
                    after_patch_api.send(
                        sender=self.model,
                        instance=instance,
                        requested_data=request.data,
                    )
                    return Response(serializer.data)
                return Response(serializer.data)

            def destroy(self, request, *args, **kwargs):
                return super(RunTimeViewset, self).destroy(
                    request=request, *args, **kwargs
                )

        return class_factory(
            class_name="{}RuntimeViewset".format(self.model.__name__),
            base_classes=(RunTimeViewset,),
        )
