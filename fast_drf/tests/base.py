from django.test import TestCase
from .test_app.models import Post
from fast_drf.utils.enums import HTTPVerbsEnum


class FastDRFTestCase(TestCase):

    def setUp(self):
        self.model = Post
        api_config = {
            'api_url': 'posts',
            'allowed_methods': [HTTPVerbsEnum.GET.value, HTTPVerbsEnum.POST.value, HTTPVerbsEnum.PUT.value],
        }

        self.api_config_kwargs = {'model': self.model}
        self.api_config_kwargs.update(**api_config)

