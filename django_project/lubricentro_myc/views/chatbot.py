from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from lubricentro_myc.models import Cliente
from lubricentro_myc.serializers.chatbot import SearchClientsSerializer
from lubricentro_myc.serializers.client import ClienteSerializer


#######################################################################
#    Set of endpoints intended to serve data to the chatbot agent.    #
#######################################################################


# TODO: add authentication
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def get_clients(request):
    serializer = SearchClientsSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(data={"errors": serializer.errors}, status=400)

    name = serializer.data["name"]
    clients = Cliente.objects.filter(nombre__icontains=name)

    serialized_data = ClienteSerializer(clients, many=True)

    return JsonResponse(data={"clients": serialized_data.data})
