import tomllib
from pathlib import Path
import argparse
from report.filehandler import MonthlyFileHandler
from tracking.tracker import TimeTracker
from statistics.stats_generator import StatsGenerator


def main(args: dict):
    with open(
        Path(__file__).parent.parent / f"{args.config.replace('.json', '')}.toml", "rb"
    ) as config_file:
        config = tomllib.load(config_file)

    # Start app
    fh = MonthlyFileHandler(config)
    tt = TimeTracker()
    report = fh.read_current_report()

    if args.workbreak:
        report = tt.work_break(report)
    elif args.stats:
        report_filename = args.stats.replace(".json", "")
        print(f"Creating stats for {report_filename}")
        statsgen = StatsGenerator()
        report = fh.read_report(fh.report_path_by_filename(report_filename))
        stats_daily_worked_minutes = statsgen.daily_worked_minutes(report)
        # TODO Decide what to do with the stats (write them to file? Directly display them in a chart?)
        print(stats_daily_worked_minutes)

    else:
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
    parser.add_argument(
        "--workbreak",
        required=False,
        action="store_true",
        help="Track the start/stop of a work break.",
    )
    parser.add_argument(
        "--stats",
        required=False,
        help="Create statistics for the given report.json file.",
    )

    args = parser.parse_args()
    main(args)
