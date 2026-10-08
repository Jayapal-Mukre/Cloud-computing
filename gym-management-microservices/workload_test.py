import time
import json
import subprocess
import os
import urllib.request
import urllib.parse
import urllib.error
from concurrent.futures import ThreadPoolExecutor

MEMBER_SERVICE_URL = "http://localhost:8001"
MEMBERSHIP_SERVICE_URL = "http://localhost:8002"
ATTENDANCE_SERVICE_URL = "http://localhost:8003"

def get_container_stats():
    stats = {}
    try:
        cmd = ["docker", "stats", "--no-stream", "--format", "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) >= 3:
                    name = parts[0].strip()
                    cpu = parts[1].strip()
                    mem = parts[2].strip().split("/")[0].strip()
                    stats[name] = {"cpu": cpu, "memory": mem}
    except Exception as e:
        print(f"Error fetching stats: {e}")
    return stats

def http_post(url):
    req = urllib.request.Request(url, data=b"", method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode())

def seed_data():
    print("--- Seeding Database ---")
    m_url = f"{MEMBER_SERVICE_URL}/members?name=Alice%20Smith&age=28&phone=9876543210&email=alice@gym.com"
    status, body = http_post(m_url)
    member_id = body.get("member_id", 1)
    print("Member creation response:", status, body)

    ms_url = f"{MEMBERSHIP_SERVICE_URL}/memberships?member_id={member_id}&plan=VIP_GOLD&start_date=2026-01-01&end_date=2026-12-31"
    status_m, body_m = http_post(ms_url)
    print("Membership creation response:", status_m, body_m)
    return member_id

def send_checkin_request(member_id):
    start_time = time.perf_counter()
    url = f"{ATTENDANCE_SERVICE_URL}/attendance/checkin?member_id={member_id}"
    try:
        req = urllib.request.Request(url, data=b"", method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            latency = (time.perf_counter() - start_time) * 1000
            return resp.status == 200, latency, resp.status
    except Exception as e:
        latency = (time.perf_counter() - start_time) * 1000
        return False, latency, 500

def run_workload_level(test_id, concurrency, total_requests, member_id):
    print(f"\n==========================================")
    print(f"Running Test {test_id}: Concurrency = {concurrency} requests, Total Requests = {total_requests}")
    print(f"==========================================")

    start_batch = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(send_checkin_request, member_id) for _ in range(total_requests)]
        results = [f.result() for f in futures]
    total_time = time.perf_counter() - start_batch

    stats = get_container_stats()
    successes = sum(1 for success, _, _ in results if success)
    failures = total_requests - successes
    latencies = [lat for _, lat, _ in results]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    min_latency = min(latencies) if latencies else 0
    max_latency = max(latencies) if latencies else 0
    throughput = total_requests / total_time if total_time > 0 else 0

    print(f"Completed in {total_time:.2f}s | Success: {successes} | Failed: {failures}")
    print(f"Avg Response Time: {avg_latency:.2f} ms | Throughput: {throughput:.2f} req/sec")

    return {
        "test_id": test_id,
        "concurrency": concurrency,
        "total_requests": total_requests,
        "successful_requests": successes,
        "failed_requests": failures,
        "total_time_sec": round(total_time, 2),
        "avg_response_time_ms": round(avg_latency, 2),
        "min_response_time_ms": round(min_latency, 2),
        "max_response_time_ms": round(max_latency, 2),
        "throughput_req_sec": round(throughput, 2),
        "container_stats": stats
    }

def main():
    member_id = seed_data()
    workloads = [("W1", 1, 30), ("W2", 2, 40), ("W3", 4, 50), ("W4", 8, 60), ("W5", 16, 80)]
    all_results = [run_workload_level(tid, conc, reqs, member_id) for tid, conc, reqs in workloads]
    with open("benchmark_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("\nBenchmark results saved to benchmark_results.json")

if __name__ == "__main__":
    main()
