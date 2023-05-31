import logging
import sys
from typing import Final
from pystray import Icon, Menu, MenuItem
from PIL import Image
from report.filehandler import MonthlyFileHandler, StatsExportFileHandler
from tracking.tracker import TimeTracker
from validation.plausibility_checker import PlausibilityChecker
from statistics.stats_generator import StatsGenerator
from statistics.stats_visualization import StatsVisualization
from util.datetimehandler import DateTimeHandler


class TrayGui:
    logger = logging.getLogger(__name__)

    ITEM_SHOW_TODAY_NAME: Final[str] = "Show Today"
    ITEM_STARTSTOP_WORK_NAME: Final[str] = "Start/Stop Work"
    ITEM_STARTSTOP_BREAK_NAME: Final[str] = "Start/Stop Break"
    ITEM_MONTHLY_STATS_NAME: Final[str] = "Monthly Statistics"
    ITEM_STATS_EXPORT: Final[str] = "Statistics Export"
    ITEM_EXIT_NAME: Final[str] = "Exit"

    LOGO_PATHS: Final[list] = [
        # dist
        "logo_64px.png",
        # developmenmt
        "src/assets/logo/logo_64px.png",
    ]

    def __init__(self, config) -> None:
        self.config = config
        self.fh = MonthlyFileHandler(self.config)
        self.efh = StatsExportFileHandler(self.config)
        self.tt = TimeTracker()
        self.pc = PlausibilityChecker()
        self.statsgen = StatsGenerator(
            default_break_after_6h=self.config["work"]["default_break_after_6h"],
            default_break_after_9h=self.config["work"]["default_break_after_9h"],
        )
        self.dth = DateTimeHandler()

    def __get_logo_image(self) -> Image:
        for path in self.LOGO_PATHS:
            try:
                return Image.open(path)
            except FileNotFoundError:
                pass
        self.logger.warn(f"Could not find logo in given paths: {self.LOGO_PATHS}")
        sys.exit(1)

    def __create_menu(self) -> Menu:
        menu_items = [
            MenuItem(self.ITEM_SHOW_TODAY_NAME, action=self.__on_show_today_clicked),
            Menu.SEPARATOR,
            MenuItem(
                self.ITEM_STARTSTOP_WORK_NAME, action=self.__on_startstop_work_clicked
            ),
            MenuItem(
                self.ITEM_STARTSTOP_BREAK_NAME, action=self.__on_workbreak_clicked
            ),
            Menu.SEPARATOR,
            MenuItem(
                self.ITEM_MONTHLY_STATS_NAME, action=self.__on_monthly_stats_clicked
            ),
            MenuItem(self.ITEM_STATS_EXPORT, action=self.__on_stats_export_clicked),
            Menu.SEPARATOR,
            MenuItem(self.ITEM_EXIT_NAME, action=lambda icon, item: icon.stop()),
        ]
        menu = Menu(*menu_items)

        return menu

    def __send_notification(self, icon: Icon, msg: str) -> None:
        if icon.HAS_NOTIFICATION:
            icon.notify(msg)

    def __send_validation_error_notification(self, icon: Icon, errors: list) -> None:
        # Always only send the first error to not overwhelm the user
        if icon.HAS_NOTIFICATION and len(errors) > 0:
            first_error = errors[0]
            icon.notify(
                f"Your report file is broken, please fix it:\n{first_error['day']}: {first_error['error']}"
            )

    def start(self):
        icon = Icon(
            "PyTimeTrack",
            icon=self.__get_logo_image(),
            menu=self.__create_menu(),
        )

        icon.run()

    def __on_startstop_work_clicked(self, icon: Icon, item: str) -> None:
        current_report = self.fh.read_current_report()
        self.logger.info(f"Validating report {self.fh.current_report_filename()}")
        report_is_valid, errors = self.pc.validate(current_report)
        if len(errors) > 0:
            self.__send_validation_error_notification(icon, errors)
        if report_is_valid:
            self.logger.info("Tracking time")
            current_report, result_msg = self.tt.track(current_report)
            self.fh.write_current_report(current_report)
            self.__send_notification(icon, result_msg)

    def __on_workbreak_clicked(self, icon: Icon, item: str) -> None:
        current_report = self.fh.read_current_report()
        self.logger.info(f"Validating report {self.fh.current_report_filename()}")
        report_is_valid, errors = self.pc.validate(current_report, check_breaks=False)
        if len(errors) > 0:
            self.__send_validation_error_notification(icon, errors)
        if report_is_valid:
            self.logger.info("Tracking work break")
            current_report, result_msg = self.tt.work_break(current_report)
            self.fh.write_current_report(current_report)

            self.__send_notification(icon, result_msg)

    def __on_monthly_stats_clicked(self, icon: Icon, item: str) -> None:
        report_filename = self.fh.current_report_filename()
        current_report = self.fh.read_current_report()
        self.logger.info(f"Validating report {report_filename}")
        report_is_valid, errors = self.pc.validate(
            current_report, check_start_end=False
        )
        if len(errors) > 0:
            self.__send_validation_error_notification(icon, errors)
        if report_is_valid:
            self.logger.info(f"Creating stats for {report_filename}")
            statsvis = StatsVisualization()
            df_stats_daily_worked_minutes = self.statsgen.daily_worked_minutes(
                report=current_report,
                target_daily_work_minutes=self.config["work"][
                    "target_daily_work_minutes"
                ],
            )
            statsvis.bar_daily_worked_minutes(
                title=f"Daily Worked Minutes ({report_filename})",
                stats=df_stats_daily_worked_minutes,
            )

    def __on_stats_export_clicked(self, icon: Icon, item: str) -> None:
        reports_paths = self.fh.list_reports_paths()
        reports_df_stats = []
        for report_path in reports_paths:
            report = self.fh.read_report(report_path)
            df_stats = self.statsgen.stats_export(
                report=report,
                target_daily_work_minutes=self.config["work"][
                    "target_daily_work_minutes"
                ],
            )
            reports_df_stats.append(df_stats)
        self.efh.write_stats_export(reports_df_stats)

    def __on_show_today_clicked(self, icon: Icon, item: str) -> None:
        current_report = self.fh.read_current_report()
        today_str, today_data = self.tt.get_today(current_report)
        if today_data is None:
            self.__send_notification(
                icon, "Could not find data for today. Start tracking first."
            )
        else:
            dt_start = self.dth.datetime_str_to_datetime(
                f"{today_str} {today_data['start']}"
            )
            dt_end = self.dth.now()
            if today_data["end"] != "":
                dt_end = self.dth.datetime_str_to_datetime(
                    f"{today_str} {today_data['end']}"
                )
            working_time = self.dth.datetime_diff_in_minutes(dt_start, dt_end)
            working_time_h = self.dth.minutes_to_full_hours(working_time)
            working_time_min = self.dth.minutes_mod_hour(working_time)
            today_info = f"Start: {today_data['start']}\nEnd: {today_data['end']}\nBreaks: {today_data['breaks']}\nWorking Time: {working_time_h}h {working_time_min}min"

            self.__send_notification(icon, today_info)
