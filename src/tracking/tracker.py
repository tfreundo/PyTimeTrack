from typing import Final
from datetime import datetime


class TimeTracker:
    TIME_FORMAT: Final[str] = "%H:%M"
    DAY_FORMAT: Final[str] = "%d.%m.%Y"
    KEY_START: Final[str] = "start"
    KEY_END: Final[str] = "end"
    KEY_WORKBREAKS: Final[str] = "breaks"
    KEY_COMMENT: Final[str] = "comment"

    def __time_now(self) -> datetime:
        return datetime.now()

    def __now_str(self) -> str:
        return self.__time_now().strftime(self.TIME_FORMAT)

    def __today_str(self) -> str:
        return self.__time_now().strftime(self.DAY_FORMAT)

    def track(self, report: dict) -> dict:
        today_str = self.__today_str()
        today_time_track = {
            self.KEY_START: "",
            self.KEY_END: "",
            self.KEY_WORKBREAKS: [],
            self.KEY_COMMENT: "",
        }

        if not (today_str in report.keys()):
            # Create empty time track
            print("Creating empty time track")
            report[today_str] = today_time_track

        if report[today_str] and report[today_str][self.KEY_START] == "":
            start_time = self.__now_str()
            print(f"Tracking start time: {start_time}")
            report[today_str][self.KEY_START] = start_time

        elif report[today_str] and report[today_str][self.KEY_START] != "":
            end_time = self.__now_str()
            print(f"Tracking end time: {end_time}")
            report[today_str][self.KEY_END] = end_time

        return report

    def work_break(self, report: dict) -> dict:
        today_str = self.__today_str()
        report[today_str][self.KEY_WORKBREAKS].append(self.__now_str())
        return report
