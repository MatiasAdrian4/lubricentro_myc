import datetime

import jwt
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from django_project import settings


def generate_jwt_token(user: User):
    payload = {
        "id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
    }

    return jwt.encode(payload, settings.LMYC_JWT_SECRET, algorithm="HS256")


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        lmyc_jwt = request.COOKIES.get(settings.LMYC_JWT_KEY)

        if not lmyc_jwt:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(
                lmyc_jwt, settings.LMYC_JWT_SECRET, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")

        try:
            user = User.objects.get(id=payload["id"])
        except User.DoesNotExist:
            raise AuthenticationFailed("Unauthenticated")

        return user, None
