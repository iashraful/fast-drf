from typing import Any

from django.db import transaction
from django.db.models import ForeignKey, Model, OneToOneField
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty


class SerializerGenerator(object):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.get('model')

    def make_runtime_serializer(self, api_version=None, **func_kwargs):
        """
        A generic serializer maker once at a time
        :param func_kwargs: all the extra params are accepted and pass to child
        :param api_version: API version string or number
        :return: return serializer class
        """
        # Define a protected _this to access outer scope
        _this = self
        api_version_fields = self.model.api_version_fields() if hasattr(self.model, 'api_version_fields') else {}
        current_version_fields = api_version_fields.get(api_version, '__all__')

        class RuntimeModelSerializer(serializers.ModelSerializer):
            def __init__(self, instance=None, data=empty, **kwargs):
                if data is not empty:
                    data = self.create_relational_data(data=data)
                self.api_version = api_version
                super(RuntimeModelSerializer, self).__init__(instance=instance, data=data, **kwargs)

            @classmethod
            def get_api_version(cls):
                return api_version

            class Meta:
                model = self.model
                fields = current_version_fields

            def create(self, validated_data: Any):
                with transaction.atomic():
                    instance = super(RuntimeModelSerializer, self).create(validated_data=validated_data)
                    return instance

            def update(self, instance: Model, validated_data: Any):
                with transaction.atomic():
                    instance = super(RuntimeModelSerializer, self).update(
                        instance=instance, validated_data=validated_data)
                    return instance

            def create_relational_data(self, data, **kwargs):
                # Getting the relational fields
                relational_fields = _this.get_relational_fields()
                # Iterate over the list
                for field in relational_fields:
                    if field.name not in data.keys():
                        # If the field is not present on the given data(User inputted data)
                        continue
                    if type(data[field.name]) == dict:
                        _model = field.related_model
                        try:
                            # Creating related data here
                            related_instance = _model.objects.create(**data[field.name])
                            data.pop(field.name)
                        except TypeError:
                            raise ValidationError({'message': _('{0} contains invalid data.'.format(field.name))})
                        # While no error and data has created then assign the PK to the serializer field.
                        data[field.name] = related_instance.pk
                return data

        return RuntimeModelSerializer

    def get_relational_fields(self, **kwargs):
        # Currently we only have support for creating One2One and ForeignKey field support
        _relational_fields = [OneToOneField, ForeignKey]
        _fields = [f for f in self.model._meta.get_fields() if f.__class__ in _relational_fields]
        return _fields
