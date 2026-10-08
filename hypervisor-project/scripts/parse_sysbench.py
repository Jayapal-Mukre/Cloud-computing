#!/usr/bin/env python3

"""Parse a Sysbench CPU result and print the important metrics.

Usage:
    python3 parse_sysbench.py benchmark_results.log
"""

import re
import sys
from pathlib import Path


PATTERNS = {
    "events_per_second": r"events per second:\s*([0-9.]+)",
    "total_time": r"total time:\s*([0-9.]+)s",
    "total_events": r"total number of events:\s*([0-9]+)",
    "min_latency": r"min:\s*([0-9.]+)",
    "avg_latency": r"avg:\s*([0-9.]+)",
    "max_latency": r"max:\s*([0-9.]+)",
    "95th_percentile": r"95th percentile:\s*([0-9.]+)",
}


def parse(text: str) -> dict:
    values = {}
    for name, pattern in PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            values[name] = float(match.group(1))
    return values


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 parse_sysbench.py <sysbench-log>")
        raise SystemExit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        raise SystemExit(1)

    values = parse(path.read_text(errors="replace"))

    print("\nSysbench CPU Results")
    print("--------------------")
    for key, value in values.items():
        unit = ""
        if "latency" in key or "percentile" in key:
            unit = " ms"
        elif key == "total_time":
            unit = " s"
        elif key == "events_per_second":
            unit = " events/s"

        if isinstance(value, float) and value.is_integer():
            value = int(value)

        print(f"{key:20}: {value}{unit}")

    if not values:
        print("No recognised Sysbench metrics were found.")


if __name__ == "__main__":
    main()
