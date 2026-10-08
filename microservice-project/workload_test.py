import concurrent.futures
import json
import statistics
import time
import requests

URL = "http://localhost:8001/health"
CONCURRENCY_LEVELS = [1, 10, 25, 50, 100]
REQUESTS_PER_LEVEL = 200

def one_request():
    start = time.perf_counter()
    try:
        response = requests.get(URL, timeout=10)
        ok = response.status_code == 200
    except requests.RequestException:
        ok = False
    return time.perf_counter() - start, ok

def run_level(concurrency):
    latencies = []
    success = 0
    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(one_request) for _ in range(REQUESTS_PER_LEVEL)]
        for future in concurrent.futures.as_completed(futures):
            latency, ok = future.result()
            latencies.append(latency)
            success += int(ok)

    elapsed = time.perf_counter() - start
    return {
        "concurrency": concurrency,
        "requests": REQUESTS_PER_LEVEL,
        "successful": success,
        "failed": REQUESTS_PER_LEVEL - success,
        "average_latency_ms": round(statistics.mean(latencies) * 1000, 3),
        "throughput_req_per_sec": round(REQUESTS_PER_LEVEL / elapsed, 3),
        "error_rate_percent": round((REQUESTS_PER_LEVEL - success) * 100 / REQUESTS_PER_LEVEL, 3)
    }

results = [run_level(level) for level in CONCURRENCY_LEVELS]
with open("benchmark_results.json", "w") as f:
    json.dump(results, f, indent=2)

for row in results:
    print(row)
