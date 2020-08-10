from copy import deepcopy

from django.db.models import Q


class APIFilteredMixin:
    """
    DO NOT INCLUDE THIS CLASS TO ANY MODEL, VIEW OR ANYWHERE

    Basically it'll parse the request params and return django queryset format
    """


    @classmethod
    def get_filters(cls, model, request, **kwargs):
        """
        model:
        """
        _fields = [f.name for f in model._meta.get_fields()]
        _params = request.GET
        _filters = {}
        for param, val in _params.items():
            try:
                if ':' in param:
                    _field_name, _filter_option = param.split(':')
                    if _field_name not in _fields:
                        continue
                    _temp = deepcopy(param)
                    _filters['{}__{}'.format(_field_name, _filter_option)] = val
                else:
                    if param not in _fields:
                        continue
                    _filters[param] = val
            except Exception as error:
                continue
        return Q(**_filters)

