from typing import Final
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from pandas import DataFrame
from util.datetimehandler import DateTimeHandler


class StatsVisualization:
    STYLE_PALETTE: Final[str] = "pastel"
    # Values can be checked in sns.axes_style()
    STYLE_THEME: Final[dict] = {
        "axes.labelcolor": "white",
        "axes.edgecolor": "white",
        "grid.color": "white",
        "text.color": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "axes.facecolor": "#183446",
        "figure.facecolor": "#022f40",
    }

    def __init__(self) -> None:
        self.dth = DateTimeHandler()
        # Seaborn style
        sns.set_theme(
            style="whitegrid",
            rc=self.STYLE_THEME,
        )

    def bar_daily_worked_minutes(self, title: str, stats: DataFrame):
        """Creates a bar chart showing the daily worked minutes, breaks and the daily target line.

        Args:
            stats (DataFrame): Statistics holding information about daily worked minutes and breaks.
        """

        fig, ax = plt.subplots(num="PyTimeTrack")

        # Transform data from wide to long format for visualization
        df_stats_vis = stats.reset_index()
        df_stats_vis.drop("default_break_minutes", axis=1, inplace=True)
        df_stats_vis.drop("total_break_minutes", axis=1, inplace=True)

        df_stats_vis = df_stats_vis.rename(
            columns={
                "total_work_minutes": "Work",
                "total_work_without_break": "Pure Work",
                "target_work_minutes": "Target",
            }
        )
        df_stats_vis = df_stats_vis.melt(
            id_vars="day",
            value_vars=[
                "Work",
                "Pure Work",
                "Target",
            ],
        )
        df_stats_vis = df_stats_vis.rename(columns={"variable": "type"})

        # Adapt plot
        ax.set_title(title)
        fig.autofmt_xdate()
        # Set plot range to always show the complete month, even if there's no data for some days
        ax.set_xlim(
            [
                self.dth.last_day_of_previous_month(),
                self.dth.first_day_of_next_month(),
            ]
        )
        xfmt = mdates.DateFormatter("%d.%m")
        ax.xaxis.set_major_formatter(xfmt)
        ax.set_xlabel("day")
        ax.set_ylabel("minutes")
        plt.grid()

        sns.lineplot(
            data=df_stats_vis,
            x="day",
            y="value",
            hue="type",
            ax=ax,
            style="type",
            markers=True,
            dashes=True,
            palette=self.STYLE_PALETTE,
        )

        plt.show()
