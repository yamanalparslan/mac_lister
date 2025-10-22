#!/usr/bin/env python3
"""
Find and print the Wi-Fi MAC address on macOS.

This script uses `networksetup -listallhardwareports` to map the "Wi-Fi" or
"AirPort" hardware port to a BSD device name (e.g. en0) and then reads the
MAC address via `ifconfig <device>`.

Works on macOS. Prints the MAC address to stdout or exits with non-zero code
on failure.
"""
import re
import shutil
import subprocess
import sys


def run(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return out.decode("utf-8", errors="ignore")
    except subprocess.CalledProcessError:
        return ""


def find_wifi_device():
    # Prefer networksetup if available because it reports human-friendly names
    if shutil.which("networksetup"):
        out = run(["networksetup", "-listallhardwareports"])
        # Example block:
        # Hardware Port: Wi-Fi
        # Device: en0
        # Ethernet Address: aa:bb:cc:dd:ee:ff
        for block in out.split("\n\n"):
            if not block.strip():
                continue
            if re.search(r"Hardware Port:\s*(Wi-?Fi|AirPort)", block, re.I):
                m = re.search(r"Device:\s*(\w+)", block)
                if m:
                    return m.group(1)
    # Fallback: check common interfaces
    for dev in ("en0", "en1", "en2"):
        if shutil.which("ifconfig"):
            out = run(["ifconfig", dev])
            if out: # commit deneme
                return dev
    return None


def get_mac_for_device(dev):
    if not dev:
        return None
    if shutil.which("ifconfig"):
        out = run(["ifconfig", dev])
        # look for ether aa:bb:cc:dd:ee:ff
        m = re.search(r"ether\s+([0-9a-f:]{17})", out, re.I)
        if m:
            return m.group(1).lower()
    return None


def main():
    dev = find_wifi_device()
    if not dev:
        print("Could not determine Wi-Fi network device (e.g. en0).", file=sys.stderr)
        sys.exit(2)
    mac = get_mac_for_device(dev)
    if not mac:
        print(f"Could not read MAC for device {dev}.", file=sys.stderr)
        sys.exit(3)
    print(mac)


if __name__ == "__main__":
    main()
