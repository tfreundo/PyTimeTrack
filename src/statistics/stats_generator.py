from typing import Final
from datetime import datetime

class StatsGenerator:
    DATETIME_FORMAT: Final[str] = "%d.%m.%Y %H:%M"

    def __datetime_diff_in_minutes(self, start: datetime, end: datetime) -> int:
        return (end - start).seconds / 60

    def daily_worked_minutes(self, report: dict) -> dict:
        """Calculates the daily worked minutes by subtracting
        the breaks based on the data in the given report.

        Args:
            report (dict): The report to use.

        Returns:
            dict: Daily worked hours with subtracted breaks.
        """
        result = {}
        for day in report.keys():
            dt_start = datetime.strptime(
                f"{day} {report[day]['start']}", self.DATETIME_FORMAT
            )
            dt_end = datetime.strptime(
                f"{day} {report[day]['end']}", self.DATETIME_FORMAT
            )
            total_work_time = self.__datetime_diff_in_minutes(dt_start, dt_end)
            # TODO total_break (if no breaks in array, use the default break setting from config?)
            total_break_time = 0.0
            breaks = report[day]["breaks"]
            if (len(breaks) % 2) != 0:
                raise AssertionError(
                    "There was an uneven number of breaks, meaning a break was started but not ended. Please fix this."
                )
            # Split into chunks of two values (start and stop of break)
            for i in range(0, len(breaks), 2):
                breaks_chunk = breaks[i : i + 2]
                dt_break_start = datetime.strptime(
                    f"{day} {breaks_chunk[0]}", self.DATETIME_FORMAT
                )
                dt_break_end = datetime.strptime(
                    f"{day} {breaks_chunk[1]}", self.DATETIME_FORMAT
                )
                break_time = self.__datetime_diff_in_minutes(
                    dt_break_start, dt_break_end
                )
                total_break_time += break_time

            result[day] = {
                "total_work_minutes": int(total_work_time),
                "total_break_minutes": int(total_break_time),
            }
        return result
