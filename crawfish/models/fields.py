from django.db import models


class EmailField(models.EmailField):

    description = "A email used for user accounts (always lowercase)."

    def __init__(self, *args, **kwargs):
        super(EmailField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            return value.lower()
        return value
