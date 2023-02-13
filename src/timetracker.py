import tomllib
from pathlib import Path
import argparse
from report.filehandler import MonthlyFileHandler
from tracking.tracker import TimeTracker


def main(args: dict):
    with open(
        Path(__file__).parent.parent / f"{args.config}.toml", "rb"
    ) as config_file:
        config = tomllib.load(config_file)

    # Start app
    fh = MonthlyFileHandler(config)
    tt = TimeTracker()
    report = fh.read_current_report()

    if args.workbreak:
        report = tt.work_break(report)
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

    args = parser.parse_args()
    main(args)
