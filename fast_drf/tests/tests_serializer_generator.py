from rest_framework.serializers import ModelSerializer

from fast_drf.core.serializer_generator import SerializerGenerator
from .base import FastDRFTestCase


class SerializerGeneratorTestCase(FastDRFTestCase):
    def setUp(self):
        super(SerializerGeneratorTestCase, self).setUp()
        self.serializer_generator = SerializerGenerator(**self.api_config_kwargs)

    def test_generate_serializer_class(self):
        _serializer_class = self.serializer_generator.make_runtime_serializer()
        self.assertTrue(issubclass(_serializer_class, ModelSerializer))
        self.assertTrue(hasattr(_serializer_class, 'Meta'))
        self.assertEqual(getattr(_serializer_class.Meta, 'model'), self.model)

    def test_serializer_versioned_fields(self):
        # Test for version v1
        version_1_serializer_class = self.serializer_generator.make_runtime_serializer(api_version='v1')
        self.assertTrue(issubclass(version_1_serializer_class, ModelSerializer))
        self.assertTrue(hasattr(version_1_serializer_class, 'Meta'))
        self.assertEqual(getattr(version_1_serializer_class.Meta, 'model'), self.model)
        self.assertEqual(self.model.api_version_fields()['v1'], version_1_serializer_class.Meta.fields)
        # Test for version v2
        version_2_serializer_class = self.serializer_generator.make_runtime_serializer(api_version='v2')
        self.assertTrue(issubclass(version_2_serializer_class, ModelSerializer))
        self.assertTrue(hasattr(version_2_serializer_class, 'Meta'))
        self.assertEqual(getattr(version_2_serializer_class.Meta, 'model'), self.model)
        self.assertEqual(self.model.api_version_fields()['v2'], version_2_serializer_class.Meta.fields)

    def test_get_relational_fields(self):
        fields = self.serializer_generator.get_relational_fields(**self.api_config_kwargs)
        self.assertTrue(isinstance(fields, list))
