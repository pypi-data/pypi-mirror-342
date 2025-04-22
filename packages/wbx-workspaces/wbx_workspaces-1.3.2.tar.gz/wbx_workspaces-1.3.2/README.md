# Webex workspaces commands utilities 

## Usage
```
Usage: python -m wbx_workspaces [OPTIONS] COMMAND [ARGS]...

Options:
  --version            Show the version and exit.
  -t, --token TEXT     Your access token. Read from AUTH_BEARER env variable
                       by default. You can find your personal token at
                       https://developer.webex.com/docs/getting-started.
  -d, --debug INTEGER  Debug level.
  --help               Show this message and exit.

Commands:
  device-status  Show device status
  devices        List devices in given location
  locations      List locations IDs
  metrics        Gather yesteray's hourly peopleCount or timeUsed metric
  workspaces     List workspaces in given location
```

## Examples
```
# list all devices  
python -m  wbx_workspaces devices

# get device diagnostics 
python -m wbx_workspaces device-status <deviceId> "Diagnostics.*.*"

# get yesterday's peopleCount hourly metric for all workspaces under a location ID in a single JSON file
python -m wbx_workspaces metrics -l <locationID> -a peopleCount 
```