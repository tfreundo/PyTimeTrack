import logging
import pandas as pd
from pandas import DataFrame
from util.datetimehandler import DateTimeHandler


class StatsGenerator:
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        default_break_after_6h: int,
        default_break_after_9h: int,
    ) -> None:
        self.default_break_after_6h = default_break_after_6h
        self.default_break_after_9h = default_break_after_9h
        self.dth = DateTimeHandler()

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
            pandas.DataFrame: Daily worked hours with subtracted breaks.
        """
        row_days = []
        row_work_times = []
        row_break_times = []
        for day in report.keys():
            try:
                dt_start = self.dth.datetime_str_to_datetime(
                    f"{day} {report[day]['start']}"
                )
                dt_end = self.dth.datetime_str_to_datetime(
                    f"{day} {report[day]['end']}"
                )
                total_work_time = self.dth.datetime_diff_in_minutes(dt_start, dt_end)
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
                    dt_break_start = self.dth.datetime_str_to_datetime(
                        f"{day} {breaks_chunk[0]}"
                    )
                    dt_break_end = self.dth.datetime_str_to_datetime(
                        f"{day} {breaks_chunk[1]}"
                    )
                    break_time = self.dth.datetime_diff_in_minutes(
                        dt_break_start, dt_break_end
                    )
                    total_break_time += break_time
                row_break_times.append(total_break_time)
                row_days.append(self.dth.date_str_to_datetime(day))
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

    def stats_export(
        self,
        report: dict,
        target_daily_work_minutes: int,
    ) -> DataFrame:
        """Calculates the statistics export.

        Args:
            report (dict): The report to use.
            target_daily_work_minutes (int): The amount of minutes of daily target work

        Returns:
            pandas.DataFrame: Statistics export.
        """
        df_daily_worked_minutes = self.daily_worked_minutes(
            report, target_daily_work_minutes
        )
        df_stats_export = df_daily_worked_minutes.copy(deep=True)

        # Work
        df_stats_export["total_work_without_break_h"] = (
            df_stats_export["total_work_without_break"] / 60
        )
        df_stats_export["total_work_without_break_h"] = df_stats_export[
            "total_work_without_break_h"
        ].astype(int)
        df_stats_export["total_work_without_break_min"] = (
            df_stats_export["total_work_without_break"] % 60
        )
        df_stats_export["total_work_without_break_min"] = df_stats_export[
            "total_work_without_break_min"
        ].astype(int)

        # Break
        df_stats_export["total_break_h"] = df_stats_export["total_break_minutes"] / 60
        df_stats_export["total_break_h"] = df_stats_export["total_break_h"].astype(int)
        df_stats_export["total_break_min"] = df_stats_export["total_break_minutes"] % 60
        df_stats_export["total_break_min"] = df_stats_export["total_break_min"].astype(
            int
        )

        return df_stats_export[
            [
                "day",
                "total_work_without_break",
                "total_work_without_break_h",
                "total_work_without_break_min",
                "total_break_minutes",
                "total_break_h",
                "total_break_min",
            ]
        ]
