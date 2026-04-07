import datetime
from django.db import IntegrityError
from django.utils import timezone
from . import selectors
from .models import PlacementApplication, Announcement

class PlacementServiceError(Exception):
    pass

class InvalidPlacementDataError(PlacementServiceError):
    pass

def create_placement_record(*, placement_type, name, ctc, year, test_score=None, test_type=""):
    if year < 2000:
        raise InvalidPlacementDataError("Year must be >= 2000")
    if ctc is not None and ctc < 0:
        raise InvalidPlacementDataError("CTC cannot be negative")
    return selectors.create_placement_record(
        placement_type=placement_type,
        name=name,
        ctc=ctc,
        year=year,
        test_score=test_score,
        test_type=test_type or "",
    )

def create_chairman_visit(*, company_name, location, visiting_date, description=""):
    if not company_name.strip():
        raise InvalidPlacementDataError("Company name is required")
    return selectors.create_chairman_visit(
        company_name=company_name,
        location=location,
        visiting_date=visiting_date,
        description=description or "",
    )

def apply_for_job(student, record):
    # BR-JM-004 Duplicate application prevention
    try:
        app = PlacementApplication.objects.create(student=student, record=record)
        return app
    except IntegrityError:
        raise InvalidPlacementDataError("You have already applied for this job.")

def withdraw_application(student, application_id):
    try:
        app = selectors.get_application_by_id(application_id)
    except PlacementApplication.DoesNotExist:
        raise InvalidPlacementDataError("Application not found.")
    
    if app.student != student:
        raise InvalidPlacementDataError("You do not own this application.")
    
    app.delete()
    return True

def manage_offer(student, application_id, action):
    # BR-IP-004 Multiple offer management
    # For now just updates the status, the complex flow can be added later
    try:
        app = selectors.get_application_by_id(application_id)
    except PlacementApplication.DoesNotExist:
        raise InvalidPlacementDataError("Application not found.")
    
    if app.student != student:
        raise InvalidPlacementDataError("You do not own this application.")
    
    if action == "accept":
        app.recruiter_status = "Accepted by Student"
    elif action == "reject":
        app.recruiter_status = "Rejected by Student"
    else:
        raise InvalidPlacementDataError("Invalid action.")
        
    app.status_updated_at = timezone.now()
    app.save()
    return app

def update_recruiter_status(recruiter_user, application_id, status):
    try:
        app = selectors.get_application_by_id(application_id)
    except PlacementApplication.DoesNotExist:
        raise InvalidPlacementDataError("Application not found.")
    
    app.recruiter_status = status
    app.status_updated_at = timezone.now()
    app.save()
    return app

def create_announcement(chairman_user, title, content, is_published=True):
    if not title.strip() or not content.strip():
        raise InvalidPlacementDataError("Title and content are required.")
    return Announcement.objects.create(
        title=title,
        content=content,
        is_published=is_published
    )

def get_placement_records(*, placement_type=None, year=None, name=None):
    return selectors.list_placement_records(
        placement_type=placement_type,
        year=year,
        name=name,
    )

def get_placement_statistics():
    return selectors.placement_statistics_by_year()

def get_chairman_visits():
    return selectors.list_chairman_visits()

def get_dashboard_summary():
    return selectors.dashboard_summary()

def generate_resume_data(student):
    # gathers all profile data
    return selectors.get_student_profile(student)
