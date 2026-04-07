from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render

from applications.globals.models import ExtraInfo, HoldsDesignation

def get_placement_context(request):
    try:
        profile = ExtraInfo.objects.get(user=request.user)
    except Exception:
        profile = None
    
    current = HoldsDesignation.objects.filter(working=request.user)
    current1 = HoldsDesignation.objects.filter(working=request.user)
    current2 = HoldsDesignation.objects.filter(working=request.user)
    
    return {
        'profile': profile,
        'current': current,
        'current1': current1,
        'current2': current2
    }

@method_decorator(login_required, name='dispatch')
class PlacementView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'schedule_tab': True,
        }
        context.update(get_placement_context(request))
        return render(request, "placementModule/placement.html", context)

@method_decorator(login_required, name='dispatch')
class StudentRecordsView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'strecord_tab': True,
        }
        context.update(get_placement_context(request))
        return render(request, "placementModule/studentrecords.html", context)

@method_decorator(login_required, name='dispatch')
class PlacementStatisticsView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'statistics_tab': True,
        }
        context.update(get_placement_context(request))
        return render(request, "placementModule/placementstatistics.html", context)

@method_decorator(login_required, name='dispatch')
class AddPlacementRecordView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'add_record_tab': True,
        }
        context.update(get_placement_context(request))
        return render(request, "placementModule/add_placement_record.html", context)

@method_decorator(login_required, name='dispatch')
class AddPlacementVisitView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'add_visit_tab': True,
        }
        context.update(get_placement_context(request))
        return render(request, "placementModule/add_placement_visits.html", context)


@method_decorator(login_required, name='dispatch')
class PlacementStatisticsView(View):
    def get(self, request, *args, **kwargs):
        profile_context = generate_profile_context(request)
        context = {
            'statistics_tab': True,
        }
        context.update(profile_context)
        return render(request, "placementModule/placementstatistics.html", context)


@method_decorator(login_required, name='dispatch')
class AddPlacementRecordView(View):
    def get(self, request, *args, **kwargs):
        profile_context = generate_profile_context(request)
        context = {
            'add_record_tab': True,
        }
        context.update(profile_context)
        return render(request, "placementModule/add_placement_record.html", context)


@method_decorator(login_required, name='dispatch')
class AddPlacementVisitView(View):
    def get(self, request, *args, **kwargs):
        profile_context = generate_profile_context(request)
        context = {
            'add_visit_tab': True,
        }
        context.update(profile_context)
        return render(request, "placementModule/add_placement_visits.html", context)
