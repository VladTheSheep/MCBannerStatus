# MCBannerStatus
Generates an image containing various data about a running Minecraft server using RCON and the library MCRcon.

Intended to be run in combination with a web server to provide live updates to a served image.

## Dependencies

 - Python 3.10>=

## Getting started

```Bash
git clone https://github.com/VladTheSheep/MCBannerStatus.git
cd MCBannerStatus
./setup.sh
```
The `setup.sh` script will setup the project for you.

 - Checks for a valid Python version
 - Creates a Python venv
 - Installs required dependencies
 - Adds `src/conf.py`
 - Adds `run.sh`

## Configuring

Before running the program, `src/conf.py` needs to be configured.

```Python

# Uses the MCRcon library to get data from the server
# Make sure RCON is enabled on the server!
MCRCON_PASSWORD = "password"
MCRCON_HOST = "127.0.0.1"
MCRCON_PORT = 25575

# Image and font to use, required
IMAGE_PATH = ""
REGULAR_FONT_PATH = ""

# Use italic fonts in certain situations, optional
ITALIC_FONT_PATH = ""

# The offset between the edge of the image and the text
# Can be set here or via runtime arguments
X_OFFSET = 64

# The size to use for fonts
# Can be set here or via runtime arguments
FONT_SIZE = 64

# The height of the text field drawed onto the image
# If not set, the height will be the image's height divided by 6
# Can be set here or via runtime arguments
FIELD_HEIGHT = None

# The opacity of the field
# Can be set here or via runtime arguments
FIELD_OPACITY = 0.5
```

## Running

The repo comes with a bash script to launch the program. To use it, make sure to set a valid path in `run.sh`

```Bash
#!/bin/bash

source env/bin/activate
python mcstatus.py -t /save/to/path
```

Invoke with `--help` or no arguments to learn more.

## Automatically updating the banner

To run the program automatically, you can use systemd or whatever you prefer. Example systemd service and timer is provided below.

#### `mcbannerstatus.service`

```
[Unit]
Description="Updates Minecraft banner"
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/path/to/MCBannerStatus
ExecStart=bash /path/to/MCBannerStatus/run.sh
```

#### `mcbannerstatus.timer`

```
[Unit]
Description=Timer for MCBannerStatus

[Timer]
OnBootSec=0min
OnUnitActiveSec=5min

[Install]
WantedBy=multi-user.target
```

You can set how often you want to update the banner by changing `OnUnitActiveSec=5min`.

Place both of these files in either `/etc/systemd/system/` or in your users systemd config `~/.config/systemd/user/`

You can enable it by enabling and starting the timer.

```Bash
# Ensure the daemon is reloaded first! Append --user if installed as a user service
systemctl daemon-reload

# If installed as a system service
systemctl enable --now mcbannerstatus.timer

# If installed as a user service
systemctl enable --now --user mcbannerstatus.timer
```
