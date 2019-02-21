from django.contrib.auth.models import User
from django.db import models

from fast_drf.mixins.expose_api_model_mixin import ExposeApiModelMixin
from fast_drf.utils.enums import HTTPVerbsEnum


class UserProfile(ExposeApiModelMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)
    address = models.TextField(verbose_name='Address')
    dob = models.DateField(null=True)

    class Meta:
        app_label = 'example_app'

    @classmethod
    def exposed_api(cls, *args, **kwargs):
        api_configs = {
            "api_url": "user-profiles",
        }
        return api_configs


class TestUser(UserProfile):
    class Meta:
        proxy = True
        app_label = 'example_app'

    @classmethod
    def exposed_api(cls, *args, **kwargs):
        api_configs = {
            "api_url": "test-users",
        }
        return api_configs


class PostMeta(models.Model):
    meta_info = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'example_app'


class Post(ExposeApiModelMixin, models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=256, null=True)
    description = models.TextField(null=True)
    meta = models.ForeignKey(PostMeta, on_delete=models.SET_NULL, null=True, related_name='posts')

    class Meta:
        app_label = 'example_app'

    @classmethod
    def exposed_api(cls, *args, **kwargs):
        from .views import PostAPIView
        from .serializers import PostPrivateSerializer

        api_configs = {
            "api_url": "posts",
            # "viewset_class": PostAPIView,
            # "serializer_class": PostPrivateSerializer,
            "allowed_methods": [HTTPVerbsEnum.GET.value, HTTPVerbsEnum.POST.value, HTTPVerbsEnum.PUT.value],
            "queryset": cls.objects.filter()
        }
        return api_configs
