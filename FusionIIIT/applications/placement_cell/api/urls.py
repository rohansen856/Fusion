from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^dashboard/$", views.placement_dashboard, name="placement-dashboard-api"),
    url(r"^records/$", views.placement_records, name="placement-records-api"),
    url(r"^statistics/$", views.placement_statistics, name="placement-statistics-api"),
    url(r"^visits/$", views.chairman_visits, name="placement-visits-api"),
]
