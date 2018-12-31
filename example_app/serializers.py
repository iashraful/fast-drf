from rest_framework.serializers import ModelSerializer

from example_app.models import Post


class PostPrivateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'description',)
