import logging
import tomllib
from pathlib import Path
import argparse
from report.filehandler import MonthlyFileHandler
from tracking.tracker import TimeTracker
from statistics.stats_generator import StatsGenerator
from statistics.stats_visualization import StatsVisualization


def main(args: dict):
    logger = logging.getLogger(__name__)
    with open(
        Path(__file__).parent.parent / f"{args.config.replace('.json', '')}.toml", "rb"
    ) as config_file:
        config = tomllib.load(config_file)

    # Initialize logging (applies to all module level loggers)
    logging.basicConfig(
        level=config["development"]["logging_level"],
        # https://docs.python.org/2/library/logging.html#logrecord-attributes
        format="%(asctime)s -- %(module)s -- (%(levelname)s): %(message)s",
        filename="output.log",
        encoding="utf-8",
    )

    # Start app
    fh = MonthlyFileHandler(config)
    tt = TimeTracker()
    current_report = fh.read_current_report()

    if args.workbreak:
        logger.info("Tracking work break")
        current_report = tt.work_break(current_report)
        fh.write_current_report(current_report)
    elif args.stats:
        # TODO Shortcut to use current_report instead of a specific report (most common use case)
        report_filename = args.stats.replace(".json", "")
        logger.info(f"Creating stats for {report_filename}")
        statsgen = StatsGenerator()
        statsvis = StatsVisualization()
        report = fh.read_report(fh.report_path_by_filename(report_filename))
        df_stats_daily_worked_minutes = statsgen.daily_worked_minutes(
            report, config["work"]["target_daily_work_minutes"]
        )
        print(df_stats_daily_worked_minutes)
        statsvis.bar_daily_worked_minutes(
            title=f"Daily Worked Minutes ({report_filename})",
            stats=df_stats_daily_worked_minutes,
        )
    else:
        logger.info("Tracking time")
        current_report = tt.track(current_report)
        fh.write_current_report(current_report)


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
