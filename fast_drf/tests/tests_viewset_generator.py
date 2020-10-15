from .base import FastDRFTestCase
from fast_drf.core.serializer_generator import SerializerGenerator
from rest_framework.serializers import ModelSerializer
from django.db.models import Model


class ViewsetGeneratorTest(FastDRFTestCase):
    def setUp(self):
        super(ViewsetGeneratorTest, self).setUp()
        self.serializer_generator = SerializerGenerator(**self.api_config_kwargs)
        self.serializer_class = self.serializer_generator.make_runtime_serializer()

    def test_generate_viewset_class(self):
        pass
