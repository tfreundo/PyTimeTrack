import pytest
import datetime
from validation.plausibility_checker import PlausibilityChecker


class TestStatsGenerator:
    @pytest.fixture
    def pc(self) -> PlausibilityChecker:
        return PlausibilityChecker()

    def test_validate_valid_report(self, pc: PlausibilityChecker):
        report = {
            "01.02.2023": {
                "start": "07:11",
                "end": "15:47",
                "breaks": ["08:12", "09:43"],
                "comment": "qweqwe",
            }
        }
        result, errors = pc.validate(report, wait_for_input=False)
        assert result == True
        assert len(errors) == 0

    def test_validate_start_after_end(self, pc: PlausibilityChecker):
        report = {
            "01.02.2023": {
                "start": "07:11",
                "end": "02:47",
                "breaks": [],
                "comment": "",
            }
        }
        result, errors = pc.validate(report, wait_for_input=False)
        assert result == False
        assert len(errors) == 1

    def test_validate_uneven_amount_of_breaks(self, pc: PlausibilityChecker):
        report = {
            "01.02.2023": {
                "start": "07:11",
                "end": "12:47",
                "breaks": ["10:20"],
                "comment": "",
            }
        }
        result, errors = pc.validate(report, wait_for_input=False)
        assert result == False
        assert len(errors) == 1

    def test_validate_break_start_after_break_end(self, pc: PlausibilityChecker):
        report = {
            "01.02.2023": {
                "start": "07:11",
                "end": "12:47",
                "breaks": ["10:20", "08:11"],
                "comment": "",
            }
        }
        result, errors = pc.validate(report, wait_for_input=False)
        assert result == False
        assert len(errors) == 1

    def test_skip_check_start_end(self, pc: PlausibilityChecker):
        report = {
            "01.02.2023": {
                "start": "15:11",
                "end": "12:47",
                "breaks": ["08:12", "09:12"],
                "comment": "",
            }
        }
        result, errors = pc.validate(
            report, wait_for_input=False, check_start_end=False
        )
        assert result == True
        assert len(errors) == 0

    def test_skip_breaks(self, pc: PlausibilityChecker):
        report = {
            "01.02.2023": {
                "start": "10:11",
                "end": "12:47",
                "breaks": ["08:12"],
                "comment": "",
            }
        }
        result, errors = pc.validate(report, wait_for_input=False, check_breaks=False)
        assert result == True
        assert len(errors) == 0
