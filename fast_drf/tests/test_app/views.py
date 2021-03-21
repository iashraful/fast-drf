from rest_framework.generics import ListCreateAPIView

from fast_drf.tests.test_app.models import Post


class PostAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
