from . import selectors


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
