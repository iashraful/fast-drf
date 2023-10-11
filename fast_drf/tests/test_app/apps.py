from django.apps import AppConfig


class FastDRFTestsConfig(AppConfig):
    name = "fast_drf.tests.test_app"
    label = "test_app"

    def ready(self):
        from fast_drf.tests.test_app import receivers
