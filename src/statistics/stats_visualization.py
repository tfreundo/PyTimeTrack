import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas import DataFrame
import numpy as np


class StatsVisualization:
    def bar_daily_worked_minutes(self, title: str, stats: DataFrame):
        """Creates a bar chart showing the daily worked minutes, breaks and the daily target line.

        Args:
            stats (DataFrame): Statistics holding information about daily worked minutes and breaks.
        """
        fig, ax = plt.subplots()
        ax.set_title(title)
        fig.autofmt_xdate()
        xfmt = mdates.DateFormatter("%d.%m")
        ax.xaxis.set_major_formatter(xfmt)
        ax.set_xlabel("day")
        ax.set_ylabel("minutes")

        x_axis = mdates.date2num(stats["day"])
        x_width = 0.3

        ax.bar(
            x_axis - x_width,
            stats["total_work_minutes"],
            width=x_width,
        )
        ax.bar(
            x_axis,
            stats["total_break_minutes"],
            width=x_width,
        )
        ax.bar(
            x_axis + x_width,
            stats["total_work_without_break"],
            width=x_width,
        )

        plt.legend(["Work", "Break", "Pure Work", "Target Work"])
        plt.axhline(y=stats["target_work_minutes"][0], color="red")
        plt.show()
