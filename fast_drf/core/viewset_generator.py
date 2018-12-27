from rest_framework import viewsets

__author__ = 'Ashraful'


class APIViewSetGenerator(object):
    @classmethod
    def make_runtime_viewset(cls, **kwargs):
        """
        Viewset Maker while it's not available on model. It's a generic viewset maker for any model
        :param func_kwargs: all the extra params are accepted and pass to child
        :return: return a viewset
        """
        class RunTimeViewset(viewsets.ViewSet):
            if self.permission_classes:
                permission_classes = self.permission_classes
            serializer_class = self.serializer_class
            queryset = self.queryset

            def list(self, request, **kwargs):
                return Response(self.serializer_class(self.queryset, many=True).data)

        return RunTimeViewset
