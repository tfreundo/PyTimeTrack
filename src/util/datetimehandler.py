from datetime import datetime
from typing import Final


class DateTimeHandler:
    DATE_FORMAT: Final[str] = "%d.%m.%Y"
    DATETIME_FORMAT: Final[str] = "%d.%m.%Y %H:%M"
    TIME_FORMAT: Final[str] = "%H:%M"

    def today(self) -> datetime:
        return datetime.today()

    def today_str(self) -> str:
        return self.now().strftime(self.DATE_FORMAT)

    def now(self) -> datetime:
        return datetime.now()

    def now_str(self) -> str:
        return self.now().strftime(self.TIME_FORMAT)

    def datetime_diff_in_minutes(self, start: datetime, end: datetime) -> int:
        return (end - start).seconds / 60

    def datetime_str_to_datetime(self, datetime_str: str) -> datetime:
        return datetime.strptime(datetime_str, self.DATETIME_FORMAT)

    def date_str_to_datetime(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, self.DATE_FORMAT)

    def minutes_to_full_hours(self, mins: float) -> int:
        return int(mins / 60)

    def minutes_mod_hour(self, mins: float) -> int:
        return int(mins % 60)
