import logging
from typing import Final
from datetime import datetime
import pandas as pd
from pandas import DataFrame


class StatsGenerator:
    DATE_FORMAT = "%d.%m.%Y"
    DATETIME_FORMAT: Final[str] = "%d.%m.%Y %H:%M"
    logger = logging.getLogger(__name__)

    def __datetime_diff_in_minutes(self, start: datetime, end: datetime) -> int:
        return (end - start).seconds / 60

    def daily_worked_minutes(
        self, report: dict, target_daily_work_minutes: int
    ) -> DataFrame:
        """Calculates the daily worked minutes by subtracting
        the breaks based on the data in the given report.

        Args:
            report (dict): The report to use.

        Returns:
            dict: Daily worked hours with subtracted breaks.
        """
        row_days = []
        row_work_times = []
        row_break_times = []
        for day in report.keys():
            try:
                dt_start = datetime.strptime(
                    f"{day} {report[day]['start']}", self.DATETIME_FORMAT
                )
                # TODO Drop the day completely, if end is not yet tracked (ongoing day)
                dt_end = datetime.strptime(
                    f"{day} {report[day]['end']}", self.DATETIME_FORMAT
                )
                total_work_time = self.__datetime_diff_in_minutes(dt_start, dt_end)
                row_work_times.append(total_work_time)
                # TODO total_break (if no breaks in array, use the default break setting from config?)
                total_break_time = 0.0
                breaks = report[day]["breaks"]
                if (len(breaks) % 2) != 0:
                    err_msg = "There was an uneven number of breaks, meaning a break was started but not ended. Can not create statistics."
                    self.logger.warn(err_msg)
                    raise AssertionError(err_msg)
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
                row_break_times.append(total_break_time)
                row_days.append(datetime.strptime(day, self.DATE_FORMAT))
            except ValueError:
                self.logger.info(f"Skipping day {day}: {report[day]}")

        df_result = pd.DataFrame(
            {
                "day": row_days,
                "total_work_minutes": row_work_times,
                "total_break_minutes": row_break_times,
            }
        )
        df_result["total_work_without_break"] = (
            df_result["total_work_minutes"] - df_result["total_break_minutes"]
        )
        df_result["target_work_minutes"] = target_daily_work_minutes
        return df_result
