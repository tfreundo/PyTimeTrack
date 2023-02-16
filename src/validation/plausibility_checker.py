import logging
from typing import Tuple
from util.datetimehandler import DateTimeHandler


class PlausibilityChecker:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.dth = DateTimeHandler()

    def __create_error(self, day: str, error: str):
        return {"day": day, "error": error}

    def validate(
        self,
        report: dict,
        check_start_end: bool = True,
        check_breaks: bool = True,
    ) -> Tuple[bool, list]:
        errors = []

        for day in report.keys():
            if report[day]["end"] != "" and check_start_end:
                dt_start = self.dth.datetime_str_to_datetime(
                    f"{day} {report[day]['start']}"
                )
                dt_end = self.dth.datetime_str_to_datetime(
                    f"{day} {report[day]['end']}"
                )

                if dt_start > dt_end:
                    errors.append(
                        self.__create_error(
                            day,
                            f"Start time {dt_start} has to be before end time {dt_end}.",
                        )
                    )

            if check_breaks:
                breaks = report[day]["breaks"]
                valid_breaks = True
                if (len(breaks) % 2) != 0:
                    valid_breaks = False
                    errors.append(
                        self.__create_error(
                            day,
                            "There was an uneven number of breaks, meaning a break was started but not ended.",
                        )
                    )

                if valid_breaks:
                    for i in range(0, len(breaks), 2):
                        breaks_chunk = breaks[i : i + 2]
                        dt_break_start = self.dth.datetime_str_to_datetime(
                            f"{day} {breaks_chunk[0]}"
                        )
                        dt_break_end = self.dth.datetime_str_to_datetime(
                            f"{day} {breaks_chunk[1]}"
                        )

                        if dt_break_start > dt_break_end:
                            errors.append(
                                self.__create_error(
                                    day,
                                    f"Break start time {dt_break_start} has to be before break end time {dt_break_end}.",
                                )
                            )

        if len(errors) == 0:
            self.logger.info("Report is valid.")
            return True, []
        error_msg = f"Report has the following errors:\n{errors}"
        self.logger.error(error_msg)

        return False, errors
