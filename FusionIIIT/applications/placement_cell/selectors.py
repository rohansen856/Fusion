import datetime

from django.db.models import Avg, Count

from .models import ChairmanVisit, PlacementRecord


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
