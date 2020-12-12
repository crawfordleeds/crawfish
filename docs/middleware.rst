==========
Middleware
==========

Crawfish includes base models and fields for better Django models.

ErrorPagesMiddleware
--------------------

Automatically override response body when requests are made using header `Content-Type: application/json` that generates
a response with status code 403, 404, or 500 response.

Add to your middleware list either last or as late as possible. This is to ensure this middleware is run early in the
response cycle to avoid supressing any other middleware int the request cycle.

More information available in the `Django documentation <https://docs.djangoproject.com/en/3.1/topics/http/middleware/#process-exception>`_.

.. code-block:: python

    MIDDLEWARE = [
        # other middleware
        "crawfish.middleware.ErrorPagesMiddleware
    ]


Future Plans
------------

* Configure static or dynamic response body content in settings.
* Decorator to enable/disable middleware on individual views.
