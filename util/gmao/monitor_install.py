#!/usr/bin/env python3
"""
Monitor a spack install log file for progress.

Usage:
    python3 monitor_install.py <logfile>          # monitor from current end (live)
    python3 monitor_install.py -f <logfile>       # scan from beginning of file
"""

import sys
import re
import time
import argparse

pattern = re.compile(r'==> Installing (\S+) \[(\d+)/(\d+)\]')


def monitor(logfile, from_start=False):
    with open(logfile) as f:
        if not from_start:
            f.seek(0, 2)  # seek to end for live monitoring
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            m = pattern.search(line)
            if m:
                pkg, current, total = m.group(1), m.group(2), m.group(3)
                pct = int(current) / int(total) * 100
                bar_len = 30
                filled = int(bar_len * int(current) / int(total))
                bar = '#' * filled + '-' * (bar_len - filled)
                print(f"[{bar}] {current:>4}/{total}  {pct:5.1f}%  {pkg}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Monitor spack install log progress")
    parser.add_argument("logfile", help="Path to the spack PBS/SLURM log file")
    parser.add_argument("-f", "--from-start", action="store_true",
                        help="Scan from beginning of file instead of tailing live")
    args = parser.parse_args()

    try:
        monitor(args.logfile, from_start=args.from_start)
    except KeyboardInterrupt:
        print("\nDone monitoring.")
    except FileNotFoundError:
        print(f"Error: file not found: {args.logfile}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
