import datetime
import json

import jwt
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from lubricentro_myc.serializers.user import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from django_project import settings


@require_http_methods(["POST"])
def crear_usuario(request):
    data = json.loads(request.body.decode("utf-8"))
    user = User.objects.create_user(
        username=data["nombre"],
        password=data["password"],
        email=data["email"],
    )
    user.save()
    return HttpResponse(status=200)


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            "id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }

        lmyc_token = jwt.encode(payload, settings.LMYC_TOKEN_SECRET, algorithm="HS256")

        response = Response()
        response.set_cookie(
            key=settings.LMYC_TOKEN_KEY, value=lmyc_token, httponly=True
        )
        response.data = {"jwt": lmyc_token}

        return response


class UserView(APIView):
    def get(self, request):
        lmyc_token = request.COOKIES.get(settings.LMYC_TOKEN_KEY)

        if not lmyc_token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(
                lmyc_token, settings.LMYC_TOKEN_SECRET, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")

        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(settings.LMYC_TOKEN_KEY)
        return response
