from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from lubricentro_myc.models import Venta
from lubricentro_myc.serializers.statistics import (
    BestAndWorstSellingProductsRequestSerializer,
)
from lubricentro_myc.utilities.date import str_to_date


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def best_and_worst_selling_products(request):
    serializer = BestAndWorstSellingProductsRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return JsonResponse(data={"errors": serializer.errors}, status=400)

    start_date = str_to_date(serializer.data["start_date"])
    end_date = str_to_date(serializer.data["end_date"])

    # filter the first "limit" products with greater amount_of_sales between
    # start and end date

    return JsonResponse(data={"products": []})
