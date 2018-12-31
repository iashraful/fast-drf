from rest_framework.generics import ListCreateAPIView

from example_app.models import Post


class PostAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
