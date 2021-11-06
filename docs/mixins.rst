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


DataclassMappingMixin
------

.. code-block:: python

    from crawfish.mixins import DataclassMappingMixin
