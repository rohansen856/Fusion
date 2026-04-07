from django.conf.urls import url
from . import views

app_name = 'placement'

urlpatterns = [
    url(r'^$', views.PlacementView.as_view(), name='placement'),
    url(r'^student_records/$', views.StudentRecordsView.as_view(), name='student_records'),
    url(r'^placement_statistics/$', views.PlacementStatisticsView.as_view(), name='placement_statistics'),
    url(r'^add_placement_record/$', views.AddPlacementRecordView.as_view(), name='add_placement_record'),
    url(r'^add_placement_visit/$', views.AddPlacementVisitView.as_view(), name='add_placement_visit'),
    
    # Placeholder routes for legacy HTML templates to resolve NoReverseMatch
    url(r'^manage_records/$', views.PlacementView.as_view(), name='manage_records'),
    url(r'^placement_record_save/$', views.PlacementView.as_view(), name='placement_record_save'),
    url(r'^delete_placement_record/$', views.PlacementView.as_view(), name='delete_placement_record'),
    url(r'^placement_visit_save/$', views.PlacementView.as_view(), name='placement_visit_save'),
    url(r'^invitation_status/$', views.PlacementView.as_view(), name='invitation_status'),
    url(r'^add_placement_schedule/$', views.PlacementView.as_view(), name='add_placement_schedule'),
    url(r'^apply_company/$', views.PlacementView.as_view(), name='apply_company'),
    url(r'^delete_invitation_status/$', views.PlacementView.as_view(), name='delete_invitation_status'),
    url(r'^delete_placement_statistics/$', views.PlacementView.as_view(), name='delete_placement_statistics'),
    url(r'^update_application_status/$', views.PlacementView.as_view(), name='update_application_status'),
    url(r'^get_reference_list/$', views.PlacementView.as_view(), name='get_reference_list'),
]
