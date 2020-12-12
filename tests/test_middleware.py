from django.test import TestCase, override_settings

from rest_framework import status
from rest_framework.test import APITestCase
from boot_django import MIDDLEWARE

FULL_MIDDLEWARE = MIDDLEWARE + ["crawfish.middleware.ErrorPagesMiddleware"]


@override_settings(MIDDLEWARE=FULL_MIDDLEWARE)
class MiddlewareTests(APITestCase):
    def test_404_request__content_type__application_json(self):
        resource = (
            "/jfdsfjdsafadsfadfkds"  # a resource that has no view/urls configured
        )
        resp = self.client.get(resource, content_type="application/json")

        self.assertEqual(resp.json().get("detail"), f"{resource} not found")
        self.assertEqual(resp._headers.get("content-type")[1], "application/json")

    def test_404_request__content_type__else(self):
        content_types = (
            "",
            "x-www-form-urlencoded",
            "multipart/form-data",
            "text/html",
            "text/plain",
        )

        resource = "/fajsklsakfds"
        for content_type in content_types:
            resp = self.client.get(resource, content_type=content_type)
            self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
            self.assertIsNot(resp._headers.get("content-type")[1], "application/json")
