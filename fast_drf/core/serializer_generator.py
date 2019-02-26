from django.db import transaction
from django.db.models import OneToOneField, ForeignKey
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty


class SerializerGenerator(object):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.get('model')

    def make_runtime_serializer(self, **func_kwargs):
        """
        A generic serializer maker once at a time
        :param func_kwargs: all the extra params are accepted and pass to child
        :return: return serializer class
        """
        # Define a protected _this to access outer scope
        _this = self

        class RuntimeModelSerializer(serializers.ModelSerializer):
            def __init__(self, instance=None, data=empty, **kwargs):
                if data is not empty:
                    data = self.create_relational_data(data=data)
                super(RuntimeModelSerializer, self).__init__(instance=instance, data=data, **kwargs)

            class Meta:
                model = self.model
                fields = '__all__'

            def create(self, attrs):
                with transaction.atomic():
                    instance = super(RuntimeModelSerializer, self).create(validated_data=attrs)
                    return instance

            def create_relational_data(self, data, **kwargs):
                relational_fields = _this.get_relational_fields()
                for field in relational_fields:
                    if field.name not in data.keys():
                        continue
                    if type(data[field.name]) == dict:
                        _model = field.related_model
                        try:
                            related_instance = _model.objects.create(**data[field.name])
                        except TypeError:
                            raise ValidationError({'message': '{0} contains invalid data.'.format(field.name)})
                        data[field.name] = related_instance.pk
                    elif type(data[field.name]) != int:
                        data.pop(field.name)
                return data

        return RuntimeModelSerializer

    def get_relational_fields(self, *kwargs):
        _relational_fields = [OneToOneField, ForeignKey]
        _fields = [f for f in self.model._meta.get_fields() if f.__class__ in _relational_fields]
        return _fields
