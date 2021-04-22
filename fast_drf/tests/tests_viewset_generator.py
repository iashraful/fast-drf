from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet

from fast_drf.core.serializer_generator import SerializerGenerator
from .base import FastDRFTestCase
from ..core.viewset_generator import APIViewSetGenerator


class ViewsetGeneratorTestCase(FastDRFTestCase):
    def setUp(self):
        super(ViewsetGeneratorTestCase, self).setUp()
        self.serializer_generator = SerializerGenerator(**self.api_config_kwargs)
        self.serializer_class = self.serializer_generator.make_runtime_serializer()
        _kwargs = {
            'model': self.model,
            'serializer_class': self.serializer_class,
            'slug_field': 'title'
        }
        self.viewset_generator = APIViewSetGenerator(**_kwargs)

    def test_generate_viewset_class(self):
        _viewset_class = self.viewset_generator.make_runtime_viewset()
        self.assertTrue(issubclass(_viewset_class, ModelViewSet))
        self.assertEqual(_viewset_class.serializer_class, self.serializer_class)
        self.assertEqual(_viewset_class.lookup_field, 'title')
