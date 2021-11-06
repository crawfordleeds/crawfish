========
Mixins
========

Crawfish includes base models and fields for better Django models.

ApiErrorsMixin
------

.. code-block:: python

    from crawfish.mixins import ApiErrorsMixin


usage::

    class MyModel(ApiErrorsMixin, models.Model):
        ...


ApiErrorsMixin adds the following attributes to the model:

    - ``errors``: a list of errors
    - ``error_messages``: a dictionary of error messages

WIP: This ^^ was generated entirely with GitHub Copilot. Come back soon for proper documentation.
DataclassMappingMixin
------

.. code-block:: python

    from crawfish.mixins import DataclassMappingMixin

usage::

    @dataclass
    class MyModel(DataclassMappingMixin):
        field1: str
        field2: str
        ...

WIP
