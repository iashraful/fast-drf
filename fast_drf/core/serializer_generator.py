from rest_framework import serializers


class SerializerGenerator(object):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.get('model')

    def make_runtime_serializer(self, **func_kwargs):
        """
        A generic serializer maker once at a time
        :param func_kwargs: all the extra params are accepted and pass to child
        :return: return serializer class
        """

        class RuntimeModelSerializer(serializers.ModelSerializer):
            class Meta:
                model = self.model
                fields = '__all__'

        return RuntimeModelSerializer
