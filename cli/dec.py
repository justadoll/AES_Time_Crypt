#!/usr/bin/env python3
"""
dec.py — TimeLock Vault CLI Decryptor
======================================
Usage:
    python dec.py <file.tlp> [--server URL] [--output PATH]

Examples:
    python dec.py secret.pdf.tlp
    python dec.py secret.pdf.tlp --output /tmp/secret.pdf
    python dec.py secret.pdf.tlp --server https://t.yourdomain.com
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

DEFAULT_SERVER = "https://t.rt0.me"


def decrypt(tlp_path: str, server: str, output: str | None) -> None:
    path = Path(tlp_path)
    if not path.exists():
        print(f"✗  File not found: {tlp_path}", file=sys.stderr)
        sys.exit(1)

    raw = path.read_bytes()

    try:
        meta      = json.loads(raw)
        original  = meta.get("original", "decrypted_file")
        unlock_at = meta.get("unlock_at", 0)
        unlock_dt = datetime.fromtimestamp(unlock_at, tz=timezone.utc)
        remaining = unlock_at - datetime.now(tz=timezone.utc).timestamp()
    except Exception:
        original, unlock_dt, remaining = "decrypted_file", None, 0

    out_path = output or (str(path.with_suffix("")) if path.suffix == ".tlp" else str(path) + ".dec")

    print(f"  file       →  {path.name}")
    if unlock_dt:
        print(f"  unlocks at →  {unlock_dt.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  server     →  {server}")
    print()

    if remaining > 60:
        parts = []
        s = int(remaining)
        if s // 86400:          parts.append(f"{s // 86400}d")
        if (s % 86400) // 3600: parts.append(f"{(s % 86400) // 3600}h")
        if (s % 3600) // 60:    parts.append(f"{(s % 3600) // 60}m")
        print(f"⚠  Still locked for ~{' '.join(parts)} — server will refuse")
        print()

    url = f"{server.rstrip('/')}/de"
    req = urllib.request.Request(url, data=raw, method="PUT",
                                 headers={"Content-Type": "application/octet-stream"})

    try:
        with urllib.request.urlopen(req) as resp:
            decrypted = resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            err = json.loads(body)
            print(f"✗  {err.get('error', 'Error')}", file=sys.stderr)
            if "message" in err:
                print(f"   {err['message']}", file=sys.stderr)
        except Exception:
            print(f"✗  Server {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"✗  Cannot reach server: {e.reason}", file=sys.stderr)
        sys.exit(1)

    Path(out_path).write_bytes(decrypted)
    print(f"✓  Decrypted  →  {out_path}")


def main():
    p = argparse.ArgumentParser(description="Decrypt a time-locked file",
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog=__doc__)
    p.add_argument("file")
    p.add_argument("--output", "-o")
    p.add_argument("--server", "-s", default=DEFAULT_SERVER)
    args = p.parse_args()
    decrypt(args.file, args.server, args.output)


if __name__ == "__main__":
    main()