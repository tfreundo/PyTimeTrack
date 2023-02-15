import logging
from typing import Final
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from report.filehandler import MonthlyFileHandler
from tracking.tracker import TimeTracker
from validation.plausibility_checker import PlausibilityChecker
from statistics.stats_generator import StatsGenerator
from statistics.stats_visualization import StatsVisualization


class TrayGui:
    logger = logging.getLogger(__name__)

    ITEM_STARTSTOP_WORK_NAME: Final[str] = "Start/Stop Work"
    ITEM_STARTSTOP_BREAK_NAME: Final[str] = "Start/Stop Break"
    ITEM_MONTHLY_STATS_NAME: Final[str] = "Monthly Statistics"
    ITEM_EXIT_NAME: Final[str] = "Exit"

    def __init__(self, config) -> None:
        self.config = config
        self.fh = MonthlyFileHandler(self.config)
        self.tt = TimeTracker()
        self.pc = PlausibilityChecker()

    def __create_image(self, width, height, fgcolor, fg2color, bgcolor):
        image = Image.new("RGB", (width, height), bgcolor)
        dc = ImageDraw.Draw(image)

        dc.ellipse(xy=(0, 0, width, height), width=6, outline=fgcolor)
        dc.line(xy=(15, 10, width / 2, height / 2), fill=fgcolor, width=8)
        dc.line(xy=(width / 2, height / 2, 58, height / 2), fill=fg2color, width=8)

        return image

    def __create_menu(self) -> Menu:
        menu_items = [
            MenuItem(
                self.ITEM_STARTSTOP_WORK_NAME, action=self.__on_startstop_work_clicked
            ),
            MenuItem(
                self.ITEM_STARTSTOP_BREAK_NAME, action=self.__on_workbreak_clicked
            ),
            MenuItem(
                self.ITEM_MONTHLY_STATS_NAME, action=self.__on_monthly_stats_clicked
            ),
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
            icon=self.__create_image(64, 64, "#C8E6C9", "#81C784", "#455A64"),
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
            statsgen = StatsGenerator(
                default_break_after_6h=self.config["work"]["default_break_after_6h"],
                default_break_after_9h=self.config["work"]["default_break_after_9h"],
            )
            statsvis = StatsVisualization()
            df_stats_daily_worked_minutes = statsgen.daily_worked_minutes(
                report=current_report,
                target_daily_work_minutes=self.config["work"][
                    "target_daily_work_minutes"
                ],
            )
            statsvis.bar_daily_worked_minutes(
                title=f"Daily Worked Minutes ({report_filename})",
                stats=df_stats_daily_worked_minutes,
            )
