from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from applications.placement_cell import services
from applications.placement_cell.api.serializers import (
    ChairmanVisitCreateSerializer,
    ChairmanVisitSerializer,
    PlacementRecordCreateSerializer,
    PlacementRecordSerializer,
    PlacementStatisticsSerializer,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def placement_dashboard(request):
    summary = services.get_dashboard_summary()
    return Response(summary, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def placement_records(request):
    if request.method == "GET":
        placement_type = request.GET.get("placement_type")
        year = request.GET.get("year")
        name = request.GET.get("name")
        year = int(year) if year else None

        records = services.get_placement_records(
            placement_type=placement_type,
            year=year,
            name=name,
        )
        serializer = PlacementRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = PlacementRecordCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        record = services.create_placement_record(**serializer.validated_data)
    except services.InvalidPlacementDataError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(PlacementRecordSerializer(record).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def placement_statistics(request):
    stats = services.get_placement_statistics()
    serializer = PlacementStatisticsSerializer(stats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def chairman_visits(request):
    if request.method == "GET":
        visits = services.get_chairman_visits()
        serializer = ChairmanVisitSerializer(visits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = ChairmanVisitCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        visit = services.create_chairman_visit(**serializer.validated_data)
    except services.InvalidPlacementDataError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(ChairmanVisitSerializer(visit).data, status=status.HTTP_201_CREATED)
