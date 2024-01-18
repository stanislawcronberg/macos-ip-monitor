# macos-ip-monitor
Minimalistic tool that scans for changes in your public IP address and triggers a macOS notification when it detects a change.

### TODO:

- [ ] Add a separate log file for application debug level
- [ ] Consider improving the Config setup (maybe just yaml or something else)
    - Creating a .env file to run the project is annoying, at the same time I don't want to share specific configuration links to Azure


## Why this was created?

- In order to have access to my database on Azure, I need to add my public IP address in the firewall settings
- Unfortunately my public IP address can change multiple times a day
- This allows me to have a notification that sends me immediately to the firewall configuration page whenever a change in my IP is detected

## Features

- Monitors for changes in the public IP address.
- Sends notifications with the new IP address.
- Optionally copies the new IP address to the clipboard.
- Can be configured to run only when a certain process is active.
- Customizable via a `.env` file for various settings.

## Configuration

Before running IP Monitor, configure the application by creating a `.env` file in the project root with the following variables:

- `IP_PROTOCOL`: The expected IP protocol (`IPv4` or `IPv6`). Default is `IPv4`.
- `PROCESS_NAME`: The name of the process to check for before running the IP Monitor. Leave blank to run without process check.
- `IP_WEBSITE`: The URL to fetch the public IP from. Default is `https://ipinfo.io`.
- `NOTIFICATION_LINK`: The URL to open when the notification is clicked. Default is `https://azure.com`.
- `LOG_FILEPATH`: Path to the log file. Default is `logs/ip_change.log`.
- `CURRENT_IP_FILEPATH`: Path to the file storing the current IP address. Default is `logs/current_ip.txt`.
- `DEBUG`: Set to `True` for debug mode. Default is `False`.
- `COPY_IP_TO_BUFFER`: Set to `True` to copy the new IP address to the clipboard. Default is `False`.

Example `.env` file:
```bash
IP_WEBSITE=https://ipinfo.io
PROCESS_NAME=dbeaver
NOTIFICATION_LINK=https://azure.com
LOG_FILEPATH=logs/ip_change.log
CURRENT_IP_FILEPATH=logs/current_ip.txt
IP_PROTOCOL=IPv4
COPY_IP_TO_BUFFER=True
DEBUG=False
```

## Creating the Python Environment

```bash
conda create -n ipmonitor python=3.11
conda activate ipmonitor
(ipmonitor) pip install -r requirements.txt
```

## Running the Application

To run IP Monitor, use the following command from the root of the project:
- You may want to set the .env DEBUG=True in order to see whether the notification triggers as expected

```bash
python src/main.py
```

## Usage and Configuring the Cronjob

- This application only really makes sense when setup to run with a cronjob.
- Remember to use absolute paths in your cronjob configuration and ensure you grant it permissions to send Notifications
    - I had to go into my `Notifications` settings in macOS and give permission for `terminal-notifier` to send notifications
    - First time you run the code it may also ask you for other permissions

### Setting up the cronjob:

In order to avoid activating/deactivating Python environments in a separate bash script, in the cronjob you should have the following structure

```bash
* * * * * cd /absolute/path/to/project/ && /absolute/path/to/python/from/your/conda/env /absolute/path/to/src/main.py >> /absolute/path/to/log/file.log 2>&1
```

This is the exact cronjob I have:

```bash
* * * * * cd /Users/stas/Documents/GitHub/macos-ip-monitor && /opt/homebrew/Caskroom/miniconda/base/envs/ipmonitor/bin/python /Users/stas/Documents/GitHub/macos-ip-monitor/src/main.py >> /Users/stas/Documents/GitHub/macos-ip-monitor/logs/cronjob.log 2>&1
```

### How to find your Python executable for your Conda environment

```bash
conda activate ipmonitor
(ipmonitor) which python
/opt/homebrew/Caskroom/miniconda/base/envs/ipmonitor/bin/python
```

## Project Structure

The project is structured as follows:

- [`src/config.py`](src/config.py): Contains the configuration class that loads settings from the `.env` file.
- [`src/logger_config.py`](src/logger_config.py): Configures the logger used across the application.
- [`src/utils/`](src/utils/): Contains utility modules for network checks, notifications, and miscellaneous functions.
- [`src/structures.py`](src/structures.py): Defines the `IpProtocol` Enum used for IP type checking.
- [`src/main.py`](src/main.py): The main script that orchestrates the IP monitoring logic.

## License

This project is licensed under the [MIT License](LICENSE).
