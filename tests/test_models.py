import datetime
from crawfish.models import BaseModel, EmailField
from django.db import models
from django.test import TestCase
from django.utils import timezone


class TestModel(BaseModel):
    """A test model using BaseModel abstract model"""

    test_field = models.CharField(max_length=500)

    class Meta:
        # App label is required for execution.
        app_label = "crawfish"

    def __str__(self):
        return f"TestModel(id: '{self.id}')"


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model = TestModel

    def test_creation(self):
        model0 = self.model.objects.create()
        print(model0)
        self.assertIsNotNone(model0)
        self.assertLessEqual(model0.created_at, timezone.now())
        self.assertGreater(
            model0.created_at, timezone.now() - datetime.timedelta(minutes=1)
        )
        self.assertLessEqual(model0.updated_at, timezone.now())
        self.assertGreater(
            model0.updated_at, timezone.now() - datetime.timedelta(minutes=1)
        )

        # We can expect created_at and updated_at to be nearly equal but not exactly
        self.assertNotEqual(model0.created_at, model0.updated_at)

    def test_update(self):
        model = self.model.objects.create()
        model.test_field = "Test value"
        model.save()
        self.assertIsInstance(model.created_at, datetime.datetime)
        self.assertIsInstance(model.updated_at, datetime.datetime)

        self.assertGreater(model.updated_at, model.created_at)


class FieldsTests(TestCase):
    pass
