from django.http import JsonResponse
from rest_framework import status
from core.services.jwt import decode_token
from core.models import User


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = decode_token(token)
            if payload:
                try:
                    request.user = User.objects.get(id=payload["sub"])
                except User.DoesNotExist:
                    request.user = None
            else:
                request.user = None
        else:
            request.user = None

        response = self.get_response(request)
        return response
    