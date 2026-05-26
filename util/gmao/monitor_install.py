#!/usr/bin/env python3
"""
Monitor a spack install log file for progress.

Usage:
    python3 monitor_install.py <logfile>          # monitor from current end (live)
    python3 monitor_install.py -f <logfile>       # scan from beginning of file (live)
    python3 monitor_install.py -r <logfile>       # read full file, print report, exit
"""

import sys
import re
import time
import argparse

pattern_installing = re.compile(r'==> Installing (\S+) \[(\d+)/(\d+)\]')
pattern_success    = re.compile(r'^\[.\]\s+\S+.*Installing (\S+)')
pattern_error      = re.compile(r'==> Error: Installation request failed')
pattern_failed_pkg = re.compile(r'^\s+(\S+)\s+\[FAILED\]')


def format_bar(current, total, bar_len=30):
    pct = int(current) / int(total) * 100
    filled = int(bar_len * int(current) / int(total))
    bar = '#' * filled + '-' * (bar_len - filled)
    return f"[{bar}] {current:>4}/{total}  {pct:5.1f}%"


def monitor(logfile, from_start=False):
    with open(logfile) as f:
        if not from_start:
            f.seek(0, 2)  # seek to end for live monitoring
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            m = pattern_installing.search(line)
            if m:
                pkg, current, total = m.group(1), m.group(2), m.group(3)
                print(f"{format_bar(current, total)}  {pkg}", flush=True)


def report(logfile):
    """Read entire file, show progress lines, then print a summary."""
    installs = []   # list of (pkg, current, total)
    errors = []     # packages that failed
    last_current = 0
    last_total = 0

    with open(logfile) as f:
        lines = f.readlines()

    for line in lines:
        m = pattern_installing.search(line)
        if m:
            pkg, current, total = m.group(1), int(m.group(2)), int(m.group(3))
            installs.append((pkg, current, total))
            last_current = current
            last_total = total
            print(f"{format_bar(current, total)}  {pkg}", flush=True)
            continue

        m = pattern_failed_pkg.search(line)
        if m:
            errors.append(m.group(1))

    # Summary
    print()
    print("=" * 60)
    if last_total:
        print(f"Packages attempted : {last_current}/{last_total}")
    else:
        print("No '==> Installing' lines found in log.")
    if errors:
        print(f"FAILED packages    : {len(errors)}")
        for e in errors:
            print(f"  - {e}")
    else:
        # Check for a generic error marker even without a parsed package name
        had_error = any(pattern_error.search(l) for l in lines)
        if had_error:
            print("FAILED             : yes (see log for details)")
        else:
            print("Result             : all attempted packages succeeded")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Monitor spack install log progress")
    parser.add_argument("logfile", help="Path to the spack PBS/SLURM log file")
    parser.add_argument("-f", "--from-start", action="store_true",
                        help="Scan from beginning of file instead of tailing live")
    parser.add_argument("-r", "--report", action="store_true",
                        help="Read full file, show progress, print summary, then exit")
    args = parser.parse_args()

    try:
        if args.report:
            report(args.logfile)
        else:
            monitor(args.logfile, from_start=args.from_start)
    except KeyboardInterrupt:
        print("\nDone monitoring.")
    except FileNotFoundError:
        print(f"Error: file not found: {args.logfile}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
