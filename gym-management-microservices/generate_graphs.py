import json
import os
import matplotlib.pyplot as plt

def generate_performance_charts(json_path="benchmark_results.json"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found!")
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    concurrency = [item["concurrency"] for item in data]
    avg_response_time = [item["avg_response_time_ms"] for item in data]
    throughput = [item["throughput_req_sec"] for item in data]

    member_cpu, membership_cpu, attendance_cpu = [], [], []
    member_mem, membership_mem, attendance_mem = [], [], []

    for item in data:
        stats = item.get("container_stats", {})
        
        def parse_cpu(val_str):
            try:
                return float(str(val_str).replace("%", "").strip())
            except:
                return 0.0

        def parse_mem(val_str):
            try:
                val = str(val_str).split("/")[0].strip()
                if "GiB" in val:
                    return float(val.replace("GiB", "").strip()) * 1024
                elif "MiB" in val:
                    return float(val.replace("MiB", "").strip())
                elif "KiB" in val:
                    return float(val.replace("KiB", "").strip()) / 1024
                elif "B" in val:
                    return float(val.replace("B", "").strip()) / (1024*1024)
                return float(val)
            except:
                return 0.0

        att_stats = stats.get("gym-attendance-service", stats.get("attendance-service", {}))
        mem_stats = stats.get("gym-member-service", stats.get("member-service", {}))
        ms_stats = stats.get("gym-membership-service", stats.get("membership-service", {}))

        attendance_cpu.append(parse_cpu(att_stats.get("cpu", "0%")))
        member_cpu.append(parse_cpu(mem_stats.get("cpu", "0%")))
        membership_cpu.append(parse_cpu(ms_stats.get("cpu", "0%")))

        attendance_mem.append(parse_mem(att_stats.get("memory", "0MiB")))
        member_mem.append(parse_mem(mem_stats.get("memory", "0MiB")))
        membership_mem.append(parse_mem(ms_stats.get("memory", "0MiB")))

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # 1. Concurrent Requests vs Average Response Time
    plt.figure(figsize=(8, 5))
    plt.plot(concurrency, avg_response_time, marker="o", color="#2563eb", linewidth=2.5, markersize=8)
    plt.title("Concurrent Requests vs Average Response Time", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Concurrent Requests", fontsize=12)
    plt.ylabel("Average Response Time (ms)", fontsize=12)
    plt.xticks(concurrency)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("chart_response_time.png", dpi=300)
    plt.close()
    print("Saved chart_response_time.png")

    # 2. Concurrent Requests vs Throughput
    plt.figure(figsize=(8, 5))
    plt.plot(concurrency, throughput, marker="s", color="#059669", linewidth=2.5, markersize=8)
    plt.title("Concurrent Requests vs Throughput", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Concurrent Requests", fontsize=12)
    plt.ylabel("Throughput (req/sec)", fontsize=12)
    plt.xticks(concurrency)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("chart_throughput.png", dpi=300)
    plt.close()
    print("Saved chart_throughput.png")

    # 3. Concurrent Requests vs CPU Utilization
    plt.figure(figsize=(8, 5))
    plt.plot(concurrency, attendance_cpu, marker="o", label="Attendance Service", color="#dc2626", linewidth=2)
    plt.plot(concurrency, member_cpu, marker="^", label="Member Service", color="#2563eb", linewidth=2)
    plt.plot(concurrency, membership_cpu, marker="s", label="Membership Service", color="#d97706", linewidth=2)
    plt.title("Concurrent Requests vs CPU Utilization (%)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Concurrent Requests", fontsize=12)
    plt.ylabel("CPU Utilization (%)", fontsize=12)
    plt.xticks(concurrency)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("chart_cpu_utilization.png", dpi=300)
    plt.close()
    print("Saved chart_cpu_utilization.png")

    # 4. Concurrent Requests vs Memory Utilization
    plt.figure(figsize=(8, 5))
    plt.plot(concurrency, attendance_mem, marker="o", label="Attendance Service", color="#dc2626", linewidth=2)
    plt.plot(concurrency, member_mem, marker="^", label="Member Service", color="#2563eb", linewidth=2)
    plt.plot(concurrency, membership_mem, marker="s", label="Membership Service", color="#d97706", linewidth=2)
    plt.title("Concurrent Requests vs Memory Utilization (MB)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Concurrent Requests", fontsize=12)
    plt.ylabel("Memory Usage (MB)", fontsize=12)
    plt.xticks(concurrency)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("chart_memory_utilization.png", dpi=300)
    plt.close()
    print("Saved chart_memory_utilization.png")

if __name__ == "__main__":
    generate_performance_charts()
