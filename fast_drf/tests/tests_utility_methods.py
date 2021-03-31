from django.db.models import Q

from fast_drf.tests.base import FastDRFTestCase
from fast_drf.utils.parser import get_default_config, get_config, parse_filters
from fast_drf.utils.predicate import is_model


# Declaring the helper classes those will be used on the tests
# Declare a non model
class TestNonModel:
    foo = 'bar'


# Fake a request class
class FakeRequest:
    def __init__(self, get={}, post={}):
        self.GET = get
        self.POST = post


class TestUtilityMethod(FastDRFTestCase):
    def test_is_model(self):
        self.assertTrue(is_model(self.model))
        self.assertFalse(is_model(TestNonModel))

    def test_get_default_config(self):
        _config = get_default_config()
        self.assertIsInstance(_config, dict)
        self.assertTrue('DEFAULT_APPLIED_APPS' in _config)
        self.assertTrue('DEFAULT_API_PREFIX' in _config)

    def test_get_config(self):
        _config = get_config()
        self.assertIsInstance(_config, dict)
        self.assertTrue('DEFAULT_APPLIED_APPS' in _config)
        self.assertTrue('DEFAULT_API_PREFIX' in _config)

    def test_parse_filters(self):
        _request = FakeRequest(get={'title:icontains': 'Test', 'description': 'Test Passed.'})
        _filters = parse_filters(model=self.model, request=_request)
        self.assertIsInstance(_filters, Q)
