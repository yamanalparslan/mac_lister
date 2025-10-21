#!/usr/bin/env bash
# Simple helper to print Wi-Fi MAC on macOS.
# Uses networksetup to find the device, then ifconfig to print the MAC.

set -euo pipefail

if ! command -v networksetup >/dev/null 2>&1; then
  echo "networksetup not found. This script is intended for macOS." >&2
  exit 2
fi

dev=$(networksetup -listallhardwareports | awk '/Hardware Port: (Wi-Fi|AirPort)/ {getline; print $2}' | head -n1)
if [ -z "$dev" ]; then
  # fallback to common device names
  for d in en0 en1 en2; do
    if ifconfig "$d" >/dev/null 2>&1; then
      dev=$d
      break
    fi
  done
fi

if [ -z "$dev" ]; then
  echo "Could not determine Wi-Fi device." >&2
  exit 3
fi

mac=$(ifconfig "$dev" | awk '/ether/ {print $2; exit}')
if [ -z "$mac" ]; then
  echo "Could not read MAC for device $dev" >&2
  exit 4
fi

echo "$mac"
