import json

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


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
