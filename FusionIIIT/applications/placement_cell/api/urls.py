from django.conf.urls import url

from . import views

app_name = 'placement_api'

urlpatterns = [
    url(r"^$", views.placement_dashboard, name="placement"),
    url(r"^dashboard/$", views.placement_dashboard, name="placement-dashboard-api"),
    url(r"^records/$", views.placement_records, name="placement-records-api"),
    url(r"^statistics/$", views.placement_statistics, name="placement-statistics-api"),
    url(r"^visits/$", views.chairman_visits, name="placement-visits-api"),
    
    # Student specific
    url(r"^profile/$", views.student_profile, name="student-profile"),
    url(r"^jobs/$", views.job_listings, name="job-listings"),
    url(r"^jobs/(?P<record_id>\d+)/apply/$", views.apply_for_job, name="apply-for-job"),
    url(r"^applications/$", views.student_applications, name="student-applications"),
    url(r"^applications/(?P<app_id>\d+)/withdraw/$", views.withdraw_application, name="withdraw-application"),
    url(r"^applications/(?P<app_id>\d+)/(?P<action>accept|reject)/$", views.manage_offer, name="manage-offer"),
    
    # TPO/Chairman
    url(r"^companies/$", views.manage_companies, name="manage-companies"),
    url(r"^announcements/$", views.announcements, name="announcements"),
    
    # Recruiter
    url(r"^recruiter/applications/$", views.recruiter_applications, name="recruiter-applications"),
    url(r"^recruiter/applications/(?P<app_id>\d+)/shortlist/$", views.recruiter_shortlist, name="recruiter-shortlist"),
]
