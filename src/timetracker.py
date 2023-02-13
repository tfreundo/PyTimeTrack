import tomllib
from datetime import datetime
import json
import os
import argparse


class TimeTracker:
    TIME_FORMAT = "%H:%M"

    def track(self, report: dict) -> dict:
        now = datetime.now()
        today_str = now.strftime("%d.%m.%Y")
        today_time_track = {"start": "", "end": "", "comment": ""}

        if not (today_str in report.keys()):
            # Create empty time track
            print("Creating empty time track")
            report[today_str] = today_time_track

        if report[today_str] and report[today_str]["start"] == "":
            start_time = now.strftime(self.TIME_FORMAT)
            print(f"Tracking start time: {start_time}")
            report[today_str]["start"] = start_time

        elif report[today_str] and report[today_str]["start"] != "":
            end_time = now.strftime(self.TIME_FORMAT)
            print(f"Tracking end time: {end_time}")
            report[today_str]["end"] = end_time

        return report


class MonthlyFileHandler:
    EMPTY_FILESTRUCTURE = {}

    def __init__(self, config: dict) -> None:
        self.config = config
        self.__create_monthly_file()

    def current_report_filename(self) -> str:
        today = datetime.today()
        return (
            f"{self.config['paths']['reports']}/{today.month}_{today.year}.json"
            if not self.config["development"]["devmode"]
            else f"{self.config['paths']['reports']}/DEV_{today.month}_{today.year}.json"
        )

    def read_current_report(self) -> dict:
        with open(self.current_report_filename(), "r") as file:
            return json.load(file)

    def write_current_report(self, report: dict) -> None:
        with open(self.current_report_filename(), "w") as file:
            file.write(json.dumps(report, indent=2))

    def __create_monthly_file(self):
        """Creates a monthly report file if non exists"""
        if os.path.exists(self.current_report_filename()):
            print(
                f'Monthly report file "{self.current_report_filename()}" already exists.'
            )
        else:
            print(f'Creating report file "{self.current_report_filename()}".')
            with open(self.current_report_filename(), "w") as file:
                file.write(json.dumps(self.EMPTY_FILESTRUCTURE, indent=2))


def main(args: dict):
    with open(args.config, "rb") as config_file:
        config = tomllib.load(config_file)

    # Start app
    fh = MonthlyFileHandler(config)
    tt = TimeTracker()
    report = fh.read_current_report()
    report = tt.track(report)
    fh.write_current_report(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PyTimeTrack - Your minimalistic time tracking tool."
    )
    parser.add_argument(
        "--config",
        required=False,
        default="config",
        help="Name of a custom config.toml file to use.",
    )

    args = parser.parse_args()
    main(args)
