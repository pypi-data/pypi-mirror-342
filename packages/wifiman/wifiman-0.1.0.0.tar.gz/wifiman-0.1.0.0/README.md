# WiFi Manager for Windows

A simple, lightweight GUI application for managing WiFi connections on Windows systems.

![WiFi Manager Screenshot](https://go.allika.eu.org/wifimanscreenshot)

## Features

- **Automatic WiFi Troubleshooting**: Detects connection issues and automatically repairs them
- **WiFi Profile Management**: Easily connect to saved WiFi networks
- **Detailed Logging**: Color-coded console output for monitoring network operations
- **Simple Interface**: Clean, dark-themed UI optimized for all screen sizes
- **Windows Native**: Designed specifically for Windows 10 and Windows 11 systems

## Installation

### Option 1: Download Executable

1. Download the latest release from the [official download page](https://go.allika.eu.org/wifimanreleases)
2. Run the `wifiman.exe` file - no installation required

### Option 2: Install via Python

```bash
# Install from PyPI
pip install wifiman

# Launch the application
wifiman
```


## Usage

### Troubleshoot WiFi
Automatically detect and fix connection issues:
- Click "Troubleshoot Wi-Fi" to start automatic repair process
- The tool will disable and re-enable your adapter if connectivity is lost

### Connect to Networks
- Click "List Wi-Fi" to see all saved network profiles
- Select a network from the dropdown
- Click "Connect" to connect to the selected network

### Monitor Activity
- All operations are logged in the console window
- Color-coded messages help identify different types of events

## System Requirements
- Windows 10 or Windows 11
- Python 3.10 or higher (for installation from source)
- Administrator privileges (for network adapter operations)

## Development
This project uses a simple Python structure:
- `main.py`: Core application code
- Built with PyInstaller for standalone executable

## License
This project is licensed under the GNU General Public License v3 (GPL-3.0).

## Author
Developed by Krishnakanth Allika (richly-human-grew[at]duck[dot]com)

## Links
- [Homepage](https://go.allika.eu.org/wifiman)
- [Source Code Repository](https://go.allika.eu.org/wifimanrepo)
- [Releases](https://go.allika.eu.org/wifimanreleases)

Copyright © 2025 Krishnakanth Allika. All rights reserved.