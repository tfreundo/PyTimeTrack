from datetime import datetime


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
