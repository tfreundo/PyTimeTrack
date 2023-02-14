import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime


class StatsVisualization:
    def bar_daily_worked_minutes(self, title: str, stats: dict):
        """Creates a bar chart showing the daily worked minutes, breaks and the daily target line.

        Args:
            stats (dict): Statistics holding information about daily worked minutes and breaks.
        """
        # x = [
        #     datetime.datetime(2010, 12, 1, 10, 0),
        #     datetime.datetime(2011, 1, 4, 9, 0),
        #     datetime.datetime(2011, 5, 5, 9, 0),
        # ]
        # TODO Centralize all time format into a module and use it from there (replace everywhere in code)
        x = [
            datetime.datetime.strptime(date, "%d.%m.%Y") for date in list(stats.keys())
        ]
        y = []
        for key, val in stats.items():
            y.append(val["total_work_minutes"])

        fig, ax = plt.subplots()
        ax.set_title(title)
        fig.autofmt_xdate()
        xfmt = mdates.DateFormatter("%d.%m")
        ax.xaxis.set_major_formatter(xfmt)
        ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
        plt.show()
