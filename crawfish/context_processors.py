from django.conf import settings


def app_name(request):

    """
    Return settings.APP_NAME in the context
    """

    return {"APP_NAME": getattr(settings, "APP_NAME", None)}
