import json
from django.http import HttpResponse

from rest_framework import status as rest_status


class ErrorPagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if "application/json" in request.content_type:
            if response.status_code == rest_status.HTTP_404_NOT_FOUND:
                data = {"detail": "{0} not found".format(request.path)}
                status = rest_status.HTTP_404_NOT_FOUND
            elif response.status_code == rest_status.HTTP_403_NOT_FOUND:
                data = {"detail": "Forbidden"}
                status = rest_status.HTTP_403_FORBIDDEN
            elif response.status_code == rest_status.HTTP_500_INTERNAL_SERVER_ERROR:
                data = {"detail": "Internal Server Error"}
                status = rest_status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                return response

            return HttpResponse(
                json.dumps(data), content_type="application/json", status=status
            )

        return response
