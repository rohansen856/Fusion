from unittest.mock import patch

from django.test import SimpleTestCase

from applications.placement_cell import services


class PlacementServicesTests(SimpleTestCase):
    def test_create_placement_record_rejects_invalid_year(self):
        with self.assertRaises(services.InvalidPlacementDataError):
            services.create_placement_record(
                placement_type="PLACEMENT",
                name="Acme",
                ctc=12.5,
                year=1999,
            )

    @patch("applications.placement_cell.services.selectors.create_placement_record")
    def test_create_placement_record_calls_selector_create(self, mock_create):
        services.create_placement_record(
            placement_type="PLACEMENT",
            name="Acme",
            ctc=12.5,
            year=2026,
            test_score=80,
            test_type="OA",
        )
        mock_create.assert_called_once()

    @patch("applications.placement_cell.services.selectors.list_placement_records")
    def test_get_records_uses_selector(self, mock_selector):
        services.get_placement_records(placement_type="PLACEMENT", year=2026, name="Acme")
        mock_selector.assert_called_once_with(
            placement_type="PLACEMENT",
            year=2026,
            name="Acme",
        )
