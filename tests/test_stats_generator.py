import pytest
import datetime
from src.statistics.stats_generator import StatsGenerator


class TestStatsGenerator:
    @pytest.fixture
    def statsgen(self) -> StatsGenerator:
        return StatsGenerator(default_break_after_6h=30, default_break_after_9h=15)

    @pytest.fixture
    def test_report(self) -> dict:
        return {
            "01.02.2023": {
                "start": "07:11",
                "end": "15:47",
                "breaks": [],
                "comment": "",
            },
            "02.02.2023": {
                "start": "06:49",
                "end": "19:12",
                "breaks": ["14:41", "16:06", "18:12", "18:23"],
                "comment": "",
            },
            "03.02.2023": {
                "start": "06:49",
                "end": "19:12",
                "breaks": [],
                "comment": "",
            },
            "04.02.2023": {
                "start": "00:02",
                "end": "04:12",
                "breaks": [],
                "comment": "",
            },
        }

    def test_daily_worked_minutes(self, statsgen: StatsGenerator, test_report: dict):
        df_result = statsgen.daily_worked_minutes(
            report=test_report, target_daily_work_minutes=480
        )

        a = df_result.loc[0]["day"]
        b = a == datetime.date(year=2023, month=2, day=1)

        assert df_result.loc[0]["day"] == datetime.date(year=2023, month=2, day=1)
        assert df_result.loc[0]["total_work_minutes"] == 516
        # Default break because worked over 6h
        assert df_result.loc[0]["total_break_minutes"] == 30
        assert df_result.loc[0]["total_work_without_break"] == 486
        assert df_result.loc[1]["day"] == datetime.date(year=2023, month=2, day=2)
        assert df_result.loc[1]["total_work_minutes"] == 743
        # No adjustment of breaks because more than default
        assert df_result.loc[1]["total_break_minutes"] == 96
        assert df_result.loc[1]["total_work_without_break"] == 647
        assert df_result.loc[2]["day"] == datetime.date(year=2023, month=2, day=3)
        assert df_result.loc[2]["total_work_minutes"] == 743
        # Default break because worked over 9h
        assert df_result.loc[2]["total_break_minutes"] == 45
        assert df_result.loc[2]["total_work_without_break"] == 698
        assert df_result.loc[3]["day"] == datetime.date(year=2023, month=2, day=4)
        assert df_result.loc[3]["total_work_minutes"] == 250
        # Worked less than 6h (no break added)
        assert df_result.loc[3]["total_break_minutes"] == 0
        assert df_result.loc[3]["total_work_without_break"] == 250

    def test_daily_worked_minutes_unplausible_breaks(self, statsgen: StatsGenerator):
        # There has to be an even number of breaks as otherwise a break has not ended
        report = {
            "01.01.2022": {
                "start": "00:00",
                "end": "15:00",
                "breaks": ["08:12"],
                "comment": "",
            }
        }
        with pytest.raises(AssertionError):
            statsgen.daily_worked_minutes(report=report, target_daily_work_minutes=480)
