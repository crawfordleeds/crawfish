from rest_framework import exceptions as rest_exceptions

from django.core.exceptions import ValidationError
from dataclasses import _FIELD, _FIELDS, dataclass, fields
from collections.abc import Mapping
from .utils import get_error_message


class ApiErrorsMixin:
    """
    Mixin that transforms Django and Python exceptions into rest_framework ones.
    Without the mixin, they return 500 status code which is not desired.
    """

    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied,
    }

    def handle_exception(self, exc):
        return super().handle_exception(self.normalize_exception(exc))
        # if isinstance(exc, tuple(self.expected_exceptions.keys())):
        #     drf_exception_class = self.expected_exceptions[exc.__class__]
        #     drf_exception = drf_exception_class(get_error_message(exc))
        #
        #     return super().handle_exception(drf_exception)
        #
        # return super().handle_exception(exc)

    @classmethod
    def normalize_exception(cls, exc):
        if isinstance(exc, tuple(cls.expected_exceptions.keys())):
            drf_exception_class = cls.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))
            return drf_exception
        return exc


def api_errors(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            raise ApiErrorsMixin.normalize_exception(e)

    return wrapper


class DataclassMappingMixin(Mapping):
    """
    This mixin allows you to use a dataclass as a mapping.

    Example:

        @dataclass
        class MyDataClass(DataclassMappingMixin):
            field1: str
            field2: str

        my_data_class = MyDataClass(field1='value1', field2='value2')
        my_data_class['field1']
        my_data_class['field2']
        my_data_class.__class__.__mro__
        my_data_class.__class__.__name__
        dict(my_data_class)
        dict(**my_data_class)
        fields(my_data_class)


    This is useful as a data transfer object-like object with Django Rest Framework services following the
    Hack Software Styleguide https://github.com/crawfordleeds/Django-Styleguide.

    For example, if you were to create a service that updates a QuerySet, you could use this to specify and validate
    the data acceptable by the service.


        class UserFields(DataclassMappingMixin):
            is_active: bool

            def __post_init__(self):
                # Here you can provide any additional validation required

        def users_update(*, users: Optional["QuerySet[User]"] = None, fields: UserFields) -> int:

            qs = users or get_user_model().objects.all()
            return qs.update(**fields)

        users_update(fields=UserFields(is_active=False))

    """

    def __iter__(self):
        return (f.name for f in fields(self))

    def __getitem__(self, key):
        field = getattr(self, _FIELDS)[key]
        if field._field_type is not _FIELD:
            raise KeyError(f"'{key}' is not a dataclass field.")
        return getattr(self, field.name)

    def __len__(self):
        return len(fields(self))
