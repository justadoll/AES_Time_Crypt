#!/usr/bin/env python3
"""
enc.py — TimeLock Vault CLI Encryptor
======================================
Usage:
    python enc.py <file> [duration] [--server URL]

Duration (default: 1month):
    1h  2h  6h  12h  1d  3d  1week  2weeks  1month  3months  6months  1year

Examples:
    python enc.py secret.pdf
    python enc.py secret.pdf 1year
    python enc.py secret.pdf 2weeks --server https://t.yourdomain.com
"""

import sys
import argparse
import urllib.request
import urllib.error
from pathlib import Path

DEFAULT_SERVER   = "https://t.rt0.me"
DEFAULT_DURATION = "1month"


def encrypt(filepath: str, duration: str, server: str) -> None:
    path = Path(filepath)
    if not path.exists():
        print(f"✗  File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    raw = path.read_bytes()
    url = f"{server.rstrip('/')}/en/{duration}"

    print(f"  file     →  {path.name}  ({len(raw):,} bytes)")
    print(f"  lock for →  {duration}")
    print(f"  server   →  {server}")
    print()

    req = urllib.request.Request(url, data=raw, method="PUT", headers={
        "Content-Type": "application/octet-stream",
        "X-Filename":   path.name,
    })

    try:
        with urllib.request.urlopen(req) as resp:
            tlp_bytes  = resp.read()
            unlock_iso = resp.headers.get("X-Unlock-ISO", "?")
    except urllib.error.HTTPError as e:
        print(f"✗  Server error {e.code}: {e.read().decode(errors='replace')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"✗  Cannot reach server: {e.reason}", file=sys.stderr)
        sys.exit(1)

    out = str(path) + ".tlp"
    Path(out).write_bytes(tlp_bytes)
    print(f"✓  Encrypted  →  {out}")
    print(f"   Unlocks at →  {unlock_iso}")


def main():
    p = argparse.ArgumentParser(description="Encrypt a file with a time-lock",
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog=__doc__)
    p.add_argument("file")
    p.add_argument("duration", nargs="?", default=DEFAULT_DURATION)
    p.add_argument("--server", "-s", default=DEFAULT_SERVER)
    args = p.parse_args()
    encrypt(args.file, args.duration, args.server)


if __name__ == "__main__":
    main()