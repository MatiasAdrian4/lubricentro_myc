from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from lubricentro_myc.models import Cliente, Producto, Venta
from lubricentro_myc.serializers.chatbot import (
    SearchClientsSerializer,
    SearchProductsSerializer,
    SearchSalesSerializer,
)
from lubricentro_myc.serializers.client import ClienteSerializer
from lubricentro_myc.serializers.product import ProductoSerializer
from lubricentro_myc.serializers.sale import VentaSerializer
from lubricentro_myc.utilities.date import str_to_date


#######################################################################
#    Set of endpoints intended to serve data to the chatbot agent.    #
#######################################################################


# TODO: re-add authentication


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


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def get_products(request):
    serializer = SearchProductsSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(data={"errors": serializer.errors}, status=400)

    detail = serializer.data.get("detail")
    category = serializer.data.get("category")

    filters = Q()
    if detail:
        filters &= Q(detalle__icontains=detail)
    if category:
        filters &= Q(categoria__icontains=category)
    products = Producto.objects.filter(filters)

    serialized_data = ProductoSerializer(products, many=True)

    return JsonResponse(data={"products": serialized_data.data})


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def get_sales(request):
    serializer = SearchSalesSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(data={"errors": serializer.errors}, status=400)

    start_data = str_to_date(serializer.data["start_date"])
    end_date = str_to_date(serializer.data["end_date"])
    sales = Venta.objects.filter(fecha__range=(start_data, end_date))

    serialized_data = VentaSerializer(sales, many=True)

    return JsonResponse(data={"sales": serialized_data.data})
