import logging
import tomllib
from pathlib import Path
import argparse

from statistics.stats_generator import StatsGenerator
from statistics.stats_visualization import StatsVisualization
from validation.plausibility_checker import PlausibilityChecker
from ui.tray_gui import TrayGui


def main(args: dict):
    with open(
        Path(__file__).parent.parent / args.config
        if args.config.endswith(".toml")
        else f"{args.config}.toml",
        "rb",
    ) as config_file:
        config = tomllib.load(config_file)

    # Initialize logging (applies to all module level loggers)
    logging.basicConfig(
        level=config["development"]["logging_level"],
        # https://docs.python.org/2/library/logging.html#logrecord-attributes
        format=f"%(asctime)s -- %(module)s | {args.config} -- (%(levelname)s): %(message)s",
        filename="output.log",
        encoding="utf-8",
    )
    ui = TrayGui(config)
    ui.start()

    # TODO I should still allow (through args) to e.g. show stats for older months

    # elif args.stats:
    #     report_filename = (
    #         args.stats if args.stats.endswith(".json") else f"{args.stats}.json"
    #     )
    #     if args.stats == "current":
    #         report_filename = fh.current_report_filename()
    #     report = fh.read_report(fh.report_path_by_filename(report_filename))
    #     logger.info(f"Validating report {report_filename}")
    #     report_is_valid = pc.validate(report)
    #     # Show the stats anyways
    #     logger.info(f"Creating stats for {report_filename}")
    #     statsgen = StatsGenerator(
    #         default_break_after_6h=config["work"]["default_break_after_6h"],
    #         default_break_after_9h=config["work"]["default_break_after_9h"],
    #     )
    #     statsvis = StatsVisualization()
    #     df_stats_daily_worked_minutes = statsgen.daily_worked_minutes(
    #         report=report,
    #         target_daily_work_minutes=config["work"]["target_daily_work_minutes"],
    #     )
    #     print(df_stats_daily_worked_minutes)
    #     statsvis.bar_daily_worked_minutes(
    #         title=f"Daily Worked Minutes ({report_filename})",
    #         stats=df_stats_daily_worked_minutes,
    #     )


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

    args = parser.parse_args()
    main(args)
