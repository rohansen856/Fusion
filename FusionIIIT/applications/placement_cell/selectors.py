import datetime
from django.db.models import Avg, Count
from .models import (
    ChairmanVisit, PlacementRecord, NotifyStudent, PlacementSchedule, 
    PlacementApplication, PlacementStatus, CompanyDetails, Announcement,
    Education, Skill, Has, Experience, Project, Achievement, Publication,
    Patent, Extracurricular, Course, StudentPlacement
)

def list_placement_records(placement_type=None, year=None, name=None):
    queryset = PlacementRecord.objects.all().order_by("-year", "name")
    if placement_type:
        queryset = queryset.filter(placement_type=placement_type)
    if year is not None:
        queryset = queryset.filter(year=year)
    if name:
        queryset = queryset.filter(name__icontains=name)
    return queryset

def placement_statistics_by_year():
    return (
        PlacementRecord.objects.values("year")
        .annotate(total_records=Count("id"), avg_ctc=Avg("ctc"))
        .order_by("-year")
    )

def list_chairman_visits():
    return ChairmanVisit.objects.all().order_by("-visiting_date", "-timestamp")

def create_placement_record(**kwargs):
    return PlacementRecord.objects.create(**kwargs)

def create_chairman_visit(**kwargs):
    return ChairmanVisit.objects.create(**kwargs)

def dashboard_summary():
    records = PlacementRecord.objects.all()
    visits = ChairmanVisit.objects.all()
    return {
        "total_records": records.count(),
        "total_companies": records.values("name").distinct().count(),
        "latest_year": records.order_by("-year").values_list("year", flat=True).first(),
        "total_visits": visits.count(),
        "upcoming_visits": visits.filter(visiting_date__gte=datetime.date.today()).count(),
    }

def get_student_profile(student):
    return {
        "education": Education.objects.filter(unique_id=student),
        "skills": Has.objects.filter(unique_id=student),
        "experience": Experience.objects.filter(unique_id=student),
        "projects": Project.objects.filter(unique_id=student),
        "achievements": Achievement.objects.filter(unique_id=student),
        "publications": Publication.objects.filter(unique_id=student),
        "patents": Patent.objects.filter(unique_id=student),
        "extracurricular": Extracurricular.objects.filter(unique_id=student),
        "courses": Course.objects.filter(unique_id=student),
        "placement_status": StudentPlacement.objects.filter(unique_id=student).first()
    }

def list_active_job_postings():
    # Can add eligibility checks logic based on student later in services
    return NotifyStudent.objects.all().order_by('-timestamp')

def get_student_applications(student):
    return PlacementApplication.objects.filter(student=student).order_by('-created_at')

def get_application_by_id(application_id):
    return PlacementApplication.objects.get(id=application_id)

def get_student_placement_status(student):
    return PlacementStatus.objects.filter(unique_id=student).order_by('-timestamp')

def list_interview_schedules():
    return PlacementSchedule.objects.all().order_by('-placement_date')

def list_companies():
    return CompanyDetails.objects.all().order_by('company_name')

def list_announcements(published_only=True):
    qs = Announcement.objects.all().order_by('-created_at')
    if published_only:
        qs = qs.filter(is_published=True)
    return qs

def list_job_applications(record_id=None):
    qs = PlacementApplication.objects.all().order_by('-created_at')
    if record_id:
        qs = qs.filter(record_id=record_id)
    return qs

def get_recruiter_applications(recruiter_user):
    companies = recruiter_user.recruitercompanyaccess_set.values_list('company_name', flat=True)
    # Finding records with 'name' matching company_name
    records = PlacementRecord.objects.filter(name__in=companies)
    return PlacementApplication.objects.filter(record__in=records)
