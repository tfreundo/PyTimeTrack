import pytest
from src.statistics.stats_generator import StatsGenerator


class TestStatsGenerator:
    @pytest.fixture
    def statsgen(self) -> StatsGenerator:
        return StatsGenerator()

    @pytest.fixture
    def test_report(self) -> dict:
        return {
            "01.02.2023": {
                "start": "07:11",
                "end": "15:47",
                "breaks": [],
                "comment": "",
            },
            "13.02.2023": {
                "start": "06:49",
                "end": "19:12",
                "breaks": ["14:41", "16:06", "18:12", "18:23"],
                "comment": "",
            },
        }

    def test_daily_worked_minutes(self, statsgen: StatsGenerator, test_report: dict):
        result = statsgen.daily_worked_minutes(test_report)
        assert result["01.02.2023"]["total_work_minutes"] == 516
        assert result["01.02.2023"]["total_break_minutes"] == 0
        assert result["13.02.2023"]["total_work_minutes"] == 743
        assert result["13.02.2023"]["total_break_minutes"] == 96

    # TODO Test assertion for uneven breaks
    # TODO Extend tests in general
