"""Generate comparison charts from manually entered benchmark results.

Edit the values in RESULTS after completing the experiment.
"""

from pathlib import Path
import matplotlib.pyplot as plt


RESULTS = {
    "Proxmox VE (Type-1)": {
        "events_per_second": 0,
        "total_events": 0,
        "average_latency": 0,
    },
    "VMware Workstation (Type-2)": {
        "events_per_second": 0,
        "total_events": 0,
        "average_latency": 0,
    },
}

OUTPUT = Path("images")
OUTPUT.mkdir(exist_ok=True)


def chart(metric: str, title: str, ylabel: str, filename: str) -> None:
    names = list(RESULTS)
    values = [RESULTS[name][metric] for name in names]

    if all(value == 0 for value in values):
        print(f"Skipping {filename}: enter real benchmark values first.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(names, values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.savefig(OUTPUT / filename, dpi=200)
    plt.close()
    print(f"Created {OUTPUT / filename}")


chart(
    "events_per_second",
    "CPU Throughput Comparison",
    "Events per second",
    "events_per_second_comparison.png",
)

chart(
    "total_events",
    "Total Sysbench Events",
    "Total events",
    "total_events_comparison.png",
)

chart(
    "average_latency",
    "Average CPU Latency",
    "Latency (ms)",
    "average_latency_comparison.png",
)
