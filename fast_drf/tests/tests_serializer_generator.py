from .base import FastDRFTestCase
from fast_drf.core.serializer_generator import SerializerGenerator
from rest_framework.serializers import ModelSerializer
from django.db.models import Model


class SerializerGeneratorTest(FastDRFTestCase):
    def setUp(self):
        super(SerializerGeneratorTest, self).setUp()
        self.serializer_generator = SerializerGenerator(**self.api_config_kwargs)

    def test_generate_serializer_class(self):
        _serializer_class = self.serializer_generator.make_runtime_serializer()
        self.assertTrue(issubclass(_serializer_class, ModelSerializer))
        self.assertTrue(hasattr(_serializer_class, 'Meta'))
        self.assertEqual(getattr(_serializer_class.Meta, 'model'), self.model)

    def test_get_relational_fields(self):
        fields = self.serializer_generator.get_relational_fields(**self.api_config_kwargs)
        self.assertTrue(isinstance(fields, list))
