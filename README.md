# PyTimeTrack
Your minimalistic time tracking tool.

## Arguments

| Argument | Description |
| -------- | ----------- |
| --config | Name of a custom config file to use. If you config filename is `myconfig.toml`, include in this argument `myconfig` |

## Configuration
You can configure PyTimeTracker to your needs using the [config.toml](./config.toml).

| Section | Param | Description |
| ------- | ----- | ----------- |
| paths | reports | The path to a folder where the reports shall be stored. |
| development | devmode | Activates (if set to true) the development mode only necessary when developing features for this app. |

To use another custom config TOML, see [Arguments](#arguments).