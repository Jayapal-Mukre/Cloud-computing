#!/bin/bash

# Cloud Computing Lab
# Type-1 vs Type-2 Hypervisor CPU Benchmark

set -u

OUTPUT_FILE="benchmark_results_$(hostname)_$(date +%Y%m%d_%H%M%S).log"

echo "============================================" | tee "$OUTPUT_FILE"
echo " Hypervisor CPU Benchmark" | tee -a "$OUTPUT_FILE"
echo "============================================" | tee -a "$OUTPUT_FILE"
echo "Date: $(date)" | tee -a "$OUTPUT_FILE"
echo "Hostname: $(hostname)" | tee -a "$OUTPUT_FILE"
echo "Kernel: $(uname -r)" | tee -a "$OUTPUT_FILE"
echo "Architecture: $(uname -m)" | tee -a "$OUTPUT_FILE"

echo "" | tee -a "$OUTPUT_FILE"
echo "--- CPU ---" | tee -a "$OUTPUT_FILE"
lscpu | grep -E "Model name|CPU\\(s\\)|Core\\(s\\) per socket|Thread\\(s\\) per core|Socket\\(s\\)" | tee -a "$OUTPUT_FILE"

echo "" | tee -a "$OUTPUT_FILE"
echo "--- Memory ---" | tee -a "$OUTPUT_FILE"
free -h | tee -a "$OUTPUT_FILE"

echo "" | tee -a "$OUTPUT_FILE"
echo "--- Root Disk ---" | tee -a "$OUTPUT_FILE"
df -h / | tee -a "$OUTPUT_FILE"

if ! command -v sysbench >/dev/null 2>&1; then
    echo "" | tee -a "$OUTPUT_FILE"
    echo "Sysbench not found. Installing..." | tee -a "$OUTPUT_FILE"
    sudo apt update
    sudo apt install sysbench -y
fi

echo "" | tee -a "$OUTPUT_FILE"
echo "--- Sysbench Version ---" | tee -a "$OUTPUT_FILE"
sysbench --version | tee -a "$OUTPUT_FILE"

echo "" | tee -a "$OUTPUT_FILE"
echo "--- CPU Benchmark: 20,000 Primes ---" | tee -a "$OUTPUT_FILE"
sysbench cpu --cpu-max-prime=20000 run | tee -a "$OUTPUT_FILE"

echo "" | tee -a "$OUTPUT_FILE"
echo "Results saved to: $OUTPUT_FILE" | tee -a "$OUTPUT_FILE"
