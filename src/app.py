import logging
import tomllib
from ui.tray_gui import TrayGui


def main():
    with open(
        "config.toml",
        "rb",
    ) as config_file:
        config = tomllib.load(config_file)

    # Initialize logging (applies to all module level loggers)
    logging.basicConfig(
        level=config["development"]["logging_level"],
        # https://docs.python.org/2/library/logging.html#logrecord-attributes
        format=f"%(asctime)s -- %(module)s -- (%(levelname)s): %(message)s",
        filename="output.log",
        encoding="utf-8",
    )
    ui = TrayGui(config)
    ui.start()

    # TODO FEATURE How long do I have to still work for today?


if __name__ == "__main__":
    main()
