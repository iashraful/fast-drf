from rest_framework.serializers import ModelSerializer

from fast_drf.tests.test_app.models import Post


class PostPrivateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'description',)
