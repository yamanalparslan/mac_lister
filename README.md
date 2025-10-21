# mac_lister
mac id lister for mac os

This repository provides two small utilities to print the Wi‑Fi (AirPort)
MAC address on macOS:

- `get_wifi_mac.py` — a Python 3 script that finds the Wi‑Fi interface and
	prints its MAC address.
- `get_wifi_mac.sh` — a lightweight shell script using `networksetup` and
	`ifconfig`.

Usage examples (macOS, zsh/bash):

```bash
# Make the scripts executable once
chmod +x get_wifi_mac.py get_wifi_mac.sh

# Run Python script
./get_wifi_mac.py

# Run shell script
./get_wifi_mac.sh
```

Both scripts will print the MAC address (lowercase) or exit with a non-zero
status and a short error message if they cannot find the device.

Pull requests welcome for additional platforms or features.
