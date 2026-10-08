import json
import os
import matplotlib.pyplot as plt

with open("benchmark_results.json") as f:
    data = json.load(f)

os.makedirs("results", exist_ok=True)

x = [r["concurrency"] for r in data]
latency = [r["average_latency_ms"] for r in data]
throughput = [r["throughput_req_per_sec"] for r in data]
errors = [r["error_rate_percent"] for r in data]

plt.figure()
plt.plot(x, latency, marker="o")
plt.xlabel("Concurrency")
plt.ylabel("Average Latency (ms)")
plt.title("Concurrency vs Average Latency")
plt.grid(True)
plt.savefig("results/latency_vs_concurrency.png", dpi=160, bbox_inches="tight")
plt.close()

plt.figure()
plt.plot(x, throughput, marker="o")
plt.xlabel("Concurrency")
plt.ylabel("Throughput (requests/sec)")
plt.title("Concurrency vs Throughput")
plt.grid(True)
plt.savefig("results/throughput_vs_concurrency.png", dpi=160, bbox_inches="tight")
plt.close()

plt.figure()
plt.plot(x, errors, marker="o")
plt.xlabel("Concurrency")
plt.ylabel("Error Rate (%)")
plt.title("Concurrency vs Error Rate")
plt.grid(True)
plt.savefig("results/error_rate_vs_concurrency.png", dpi=160, bbox_inches="tight")
plt.close()

print("Graphs generated in results/")
