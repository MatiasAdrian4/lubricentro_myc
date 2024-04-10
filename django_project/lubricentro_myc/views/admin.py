from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from lubricentro_myc.models import Activity
from lubricentro_myc.serializers.activity import ActivitySerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def activities_list(_):
    serializer = ActivitySerializer(Activity.objects.all(), many=True)
    return JsonResponse(data={"activities": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def activity_details(_, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return HttpResponse(status=404)

    serializer = ActivitySerializer(activity)
    return JsonResponse(data=serializer.data)
