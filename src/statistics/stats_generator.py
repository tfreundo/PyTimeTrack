import logging
from typing import Final
from datetime import datetime
import pandas as pd
from pandas import DataFrame


class StatsGenerator:
    DATE_FORMAT = "%d.%m.%Y"
    DATETIME_FORMAT: Final[str] = "%d.%m.%Y %H:%M"
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        default_break_after_6h: int,
        default_break_after_9h: int,
    ) -> None:
        self.default_break_after_6h = default_break_after_6h
        self.default_break_after_9h = default_break_after_9h

    def datetime_diff_in_minutes(self, start: datetime, end: datetime) -> int:
        return (end - start).seconds / 60

    def __apply_calc_default_breaks(self, row) -> int:
        """Calculates the default breaks for the time worked

        Args:
            row: A row of the DataFrame

        Returns:
            int: The amount of default breaks in minutes
        """
        default_break = 0
        if row["total_work_minutes"] >= 360 and row["total_work_minutes"] < 540:
            default_break += self.default_break_after_6h
        if row["total_work_minutes"] >= 540:
            default_break += self.default_break_after_6h + self.default_break_after_9h
        return default_break

    def __apply_default_breaks(self, row):
        """Applies the default breaks on the col total_break_minutes if necessary

        Args:
            row: A row of the DataFrame

        Returns:
            int: The adapted break minutes
        """
        if row["total_break_minutes"] < row["default_break_minutes"]:
            return row["default_break_minutes"]
        else:
            return row["total_break_minutes"]

    def daily_worked_minutes(
        self,
        report: dict,
        target_daily_work_minutes: int,
    ) -> DataFrame:
        """Calculates the daily worked minutes by subtracting
        the breaks based on the data in the given report.

        Args:
            report (dict): The report to use.
            target_daily_work_minutes (int): The amount of minutes of daily target work

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
                dt_end = datetime.strptime(
                    f"{day} {report[day]['end']}", self.DATETIME_FORMAT
                )
                total_work_time = self.datetime_diff_in_minutes(dt_start, dt_end)
                row_work_times.append(total_work_time)
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
                    break_time = self.datetime_diff_in_minutes(
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
        # Include default breaks (e.g. given by working time laws)
        df_result["default_break_minutes"] = df_result.apply(
            self.__apply_calc_default_breaks, axis=1
        )
        # Adapt the total_breaks if they are not high enough
        df_result["total_break_minutes"] = df_result.apply(
            self.__apply_default_breaks, axis=1
        )

        # Calculate the pure working time
        df_result["total_work_without_break"] = (
            df_result["total_work_minutes"] - df_result["total_break_minutes"]
        )

        # Include the target working hours from config
        df_result["target_work_minutes"] = target_daily_work_minutes

        return df_result
