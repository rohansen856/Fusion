from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from applications.placement_cell import services, selectors
from applications.placement_cell.api import serializers
from applications.placement_cell.api.permissions import IsStudent, IsTPO, IsChairman, IsRecruiter
from applications.placement_cell.models import PlacementRecord

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
        serializer = serializers.PlacementRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if not IsTPO().has_permission(request, None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = serializers.PlacementRecordCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        record = services.create_placement_record(**serializer.validated_data)
    except services.InvalidPlacementDataError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializers.PlacementRecordSerializer(record).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def placement_statistics(request):
    stats = services.get_placement_statistics()
    serializer = serializers.PlacementStatisticsSerializer(stats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def chairman_visits(request):
    if request.method == "GET":
        visits = services.get_chairman_visits()
        serializer = serializers.ChairmanVisitSerializer(visits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if not IsTPO().has_permission(request, None) and not IsChairman().has_permission(request, None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = serializers.ChairmanVisitCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        visit = services.create_chairman_visit(**serializer.validated_data)
    except services.InvalidPlacementDataError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializers.ChairmanVisitSerializer(visit).data, status=status.HTTP_201_CREATED)


# --- NEW ENDPOINTS ---

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def student_profile(request):
    profile = selectors.get_student_profile(request.user.extrainfo.student)
    # Return simple dict representation for now
    return Response({
        "education": serializers.EducationSerializer(profile["education"], many=True).data,
        "skills": serializers.HasSerializer(profile["skills"], many=True).data,
        "experience": serializers.ExperienceSerializer(profile["experience"], many=True).data,
        "projects": serializers.ProjectSerializer(profile["projects"], many=True).data,
        "achievements": serializers.AchievementSerializer(profile["achievements"], many=True).data,
    }, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def job_listings(request):
    jobs = selectors.list_active_job_postings()
    serializer = serializers.NotifyStudentSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsStudent])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def apply_for_job(request, record_id):
    student = request.user.extrainfo.student
    record = get_object_or_404(PlacementRecord, id=record_id)
    try:
        app = services.apply_for_job(student, record)
        return Response(serializers.PlacementApplicationSerializer(app).data, status=status.HTTP_201_CREATED)
    except services.InvalidPlacementDataError as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def student_applications(request):
    student = request.user.extrainfo.student
    apps = selectors.get_student_applications(student)
    return Response(serializers.PlacementApplicationSerializer(apps, many=True).data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsStudent])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def manage_offer(request, app_id, action):
    student = request.user.extrainfo.student
    try:
        app = services.manage_offer(student, app_id, action)
        return Response(serializers.PlacementApplicationSerializer(app).data, status=status.HTTP_200_OK)
    except services.InvalidPlacementDataError as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsStudent])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def withdraw_application(request, app_id):
    student = request.user.extrainfo.student
    try:
        services.withdraw_application(student, app_id)
        return Response({"detail": "Application withdrawn successfully."}, status=status.HTTP_200_OK)
    except services.InvalidPlacementDataError as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def manage_companies(request):
    if not IsTPO().has_permission(request, None):
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method == "GET":
        companies = selectors.list_companies()
        return Response(serializers.CompanyDetailsSerializer(companies, many=True).data, status=status.HTTP_200_OK)
    
    # POST
    serializer = serializers.CompanyDetailsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def announcements(request):
    if request.method == "GET":
        # Students see published, TPO/Chairman see all
        published_only = IsStudent().has_permission(request, None)
        anncs = selectors.list_announcements(published_only)
        return Response(serializers.AnnouncementSerializer(anncs, many=True).data, status=status.HTTP_200_OK)
    
    # POST (Chairman only)
    if not IsChairman().has_permission(request, None):
        return Response(status=status.HTTP_403_FORBIDDEN)
        
    serializer = serializers.AnnouncementCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    annc = services.create_announcement(request.user, **serializer.validated_data)
    return Response(serializers.AnnouncementSerializer(annc).data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsRecruiter])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def recruiter_applications(request):
    apps = selectors.get_recruiter_applications(request.user)
    return Response(serializers.PlacementApplicationSerializer(apps, many=True).data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsRecruiter])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def recruiter_shortlist(request, app_id):
    status_str = request.data.get('status')
    if not status_str:
        return Response({"detail": "status is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        app = services.update_recruiter_status(request.user, app_id, status_str)
        return Response(serializers.PlacementApplicationSerializer(app).data, status=status.HTTP_200_OK)
    except services.InvalidPlacementDataError as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
