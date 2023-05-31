import logging
from typing import Final, Tuple
from util.datetimehandler import DateTimeHandler


class TimeTracker:
    logger = logging.getLogger(__name__)
    KEY_START: Final[str] = "start"
    KEY_END: Final[str] = "end"
    KEY_WORKBREAKS: Final[str] = "breaks"
    KEY_COMMENT: Final[str] = "comment"

    def __init__(self) -> None:
        self.dth = DateTimeHandler()

    def track(self, report: dict) -> Tuple[dict, str]:
        """Tracks start or stop of working

        Args:
            report (dict): The report to use

        Returns:
            Tuple[dict, str]: The updated report and a message what was updated
        """
        today_str = self.dth.today_str()
        today_time_track = {
            self.KEY_START: "",
            self.KEY_END: "",
            self.KEY_WORKBREAKS: [],
            self.KEY_COMMENT: "",
        }

        result_msg = ""

        if not (today_str in report.keys()):
            # Create empty time track
            self.logger.info("Creating empty time track")
            report[today_str] = today_time_track

        if report[today_str]:
            # There was no start time yet
            if report[today_str][self.KEY_START] == "":
                start_time = self.dth.now_time_str()
                result_msg = f"Tracked work start time: {start_time}"
                self.logger.info(result_msg)
                report[today_str][self.KEY_START] = start_time

            # There was no end time yet
            elif report[today_str][self.KEY_START] != "":
                end_time = self.dth.now_time_str()
                result_msg = f"Tracked work end time: {end_time}"
                self.logger.info(result_msg)
                report[today_str][self.KEY_END] = end_time

        return (report, result_msg)

    def work_break(self, report: dict) -> Tuple[dict, str]:
        """Tracks start or stop of a working break

        Args:
            report (dict): The report to use

        Returns:
            Tuple[dict, str]: The updated report and a message what was updated
        """
        today_str = self.dth.today_str()
        break_time = self.dth.now_time_str()
        report[today_str][self.KEY_WORKBREAKS].append(break_time)
        result_msg = f"Tracked break start time: {break_time}"
        if len(report[today_str][self.KEY_WORKBREAKS]) % 2 == 0:
            result_msg = f"Tracked break end time: {break_time}"
        self.logger.info(result_msg)
        return (report, result_msg)

    def get_today(self, report: dict) -> Tuple[str, dict]:
        """Returns the data of today

        Args:
            report (dict): The report to extract the data of today from

        Returns:
            Tuple[str, dict]: Tuple of the day and the data
        """
        today_str = self.dth.today_str()
        if today_str in report.keys():
            return today_str, report[today_str]
        return today_str, None
