from django.contrib.auth.models import User
from lubricentro_myc.authentication import generate_jwt_token
from lubricentro_myc.serializers.user import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from django_project import settings


class SignupView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(username=serializer.data.get("username"))
        lmyc_jwt = generate_jwt_token(user)

        response = Response()
        response.set_cookie(key=settings.LMYC_JWT_KEY, value=lmyc_jwt, httponly=True)

        return response


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        lmyc_jwt = generate_jwt_token(user)

        response = Response()
        response.set_cookie(key=settings.LMYC_JWT_KEY, value=lmyc_jwt, httponly=True)
        response.data = {"lmyc_jwt": lmyc_jwt}

        return response


class UserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(settings.LMYC_JWT_KEY)
        return response
