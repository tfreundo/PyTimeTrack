import json
import os
import logging
from util.datetimehandler import DateTimeHandler


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
        return f"{self.config['paths']['reports']}/{report_name}"

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
