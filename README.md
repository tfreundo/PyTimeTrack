# PyTimeTrack
Your minimalistic time tracking tool.

## Arguments

| Argument | Description |
| -------- | ----------- |
| --config | Name of a custom config file to use. If you config filename is `myconfig.toml`, use in this argument `myconfig` |
| --stats | Create statistics for the given report. If you want stats for e.g. `02_2023.json`, use in this argument `02_2023`. For the current report use the keyword `current` |

## Configuration
You can configure PyTimeTracker to your needs using the [config.toml](./config.toml).

| Section | Param | Description |
| ------- | ----- | ----------- |
| work | target_daily_work_minutes | The amount of minutes you have to work per day |
| paths | reports | The path to a folder where the reports shall be stored. |
| development | devmode | Activates (if set to true) the development mode only necessary when developing features for this app. |

To use another custom config TOML, see [Arguments](#arguments).