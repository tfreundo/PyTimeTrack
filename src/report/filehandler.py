import json
import os
import logging
from util.datetimehandler import DateTimeHandler
from glob import glob
from mdutils.mdutils import MdUtils
from pandas import DataFrame, Timestamp


class MonthlyFileHandler:
    EMPTY_FILESTRUCTURE = {}
    logger = logging.getLogger(__name__)

    def __init__(self, config: dict) -> None:
        self.config = config
        self.dth = DateTimeHandler()
        self.__create_monthly_file()

    def current_report_filename(self) -> str:
        today = self.dth.today()
        return (
            f"{today.month}_{today.year}.json"
            if not self.config["development"]["devmode"]
            else f"DEV_{today.month}_{today.year}.json"
        )

    def report_path_by_filename(self, report_name: str) -> str:
        return f"{self.get_report_path()}/{report_name}"

    def get_report_path(self) -> str:
        return f"{self.config['paths']['reports']}"

    def list_reports_paths(self) -> list[str]:
        paths = glob(f"{self.get_report_path()}/*.json")
        return paths

    def read_report(self, report_path: str):
        with open(report_path, "r") as file:
            return json.load(file)

    def read_current_report(self) -> dict:
        return self.read_report(
            self.report_path_by_filename(self.current_report_filename())
        )

    def write_current_report(self, report: dict) -> None:
        with open(
            self.report_path_by_filename(self.current_report_filename()), "w"
        ) as file:
            file.write(json.dumps(report, indent=2))

    def __create_monthly_file(self):
        """Creates a monthly report file if non exists"""
        if os.path.exists(self.report_path_by_filename(self.current_report_filename())):
            self.logger.info(
                f'Monthly report file "{self.report_path_by_filename(self.current_report_filename())}" already exists.'
            )
        else:
            self.logger.info(
                f'Creating report file "{self.report_path_by_filename(self.current_report_filename())}".'
            )
            with open(
                self.report_path_by_filename(self.current_report_filename()), "w"
            ) as file:
                file.write(json.dumps(self.EMPTY_FILESTRUCTURE, indent=2))


class StatsExportFileHandler:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.dth = DateTimeHandler()

    def get_report_path(self) -> str:
        return f"{self.config['paths']['reports']}"

    def write_stats_export(self, reports_df_stats: list[DataFrame]):
        mdFile = MdUtils(
            author="PyTimeTrack",
            file_name=f"{self.get_report_path()}/{self.dth.now_datetime_file_str()}_PyTimeTrack_Report",
            title="PyTimeTrack Report",
        )

        for df_stats in reports_df_stats:
            df_stats.sort_values(by=["day"], inplace=True)
            first_day_in_report = df_stats.iloc[0]["day"]
            # Headline for each month
            mdFile.new_header(
                level=1,
                title=f"{first_day_in_report.month_name()} {first_day_in_report.year}",
            )

            # Table with every tracked day for each month
            table_days = ["Day", "Work", "Break"]
            counter = 0
            for index, row in df_stats.iterrows():
                day: Timestamp = row["day"]
                work = f"{row['total_work_without_break_h']}h {row['total_work_without_break_min']}min"
                breaks = f"{row['total_break_h']}h {row['total_break_min']}min"
                table_days.extend([day.strftime(self.dth.DATE_FORMAT), work, breaks])
                counter += 1
            mdFile.new_line()
            table_col_qty = 3
            # All rows of DataFrame and the header
            table_row_qty = df_stats.shape[0] + 1
            mdFile.new_table(
                columns=table_col_qty,
                rows=table_row_qty,
                text=table_days,
                text_align="center",
            )
            mdFile.new_line()
            total_work_in_month_mins = df_stats["total_work_without_break"].sum()
            mdFile.write(
                f"Total work: {self.dth.minutes_to_full_hours(total_work_in_month_mins)}h {self.dth.minutes_mod_hour(total_work_in_month_mins)}min"
            )

        mdFile.new_table_of_contents(table_title="Contents", depth=1)
        mdFile.create_md_file()
