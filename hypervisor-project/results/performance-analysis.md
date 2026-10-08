# Hypervisor Performance Analysis

## Experiment

Comparison of:

- Type-1 hypervisor: Proxmox VE
- Type-2 hypervisor: VMware Workstation

Benchmark:

```bash
sysbench cpu --cpu-max-prime=20000 run
```

## Results

Replace the following table with the **actual measurements from your own VMs**.

| Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) |
|---|---:|---:|
| Total execution time | TBD | TBD |
| Total events | TBD | TBD |
| Events per second | TBD | TBD |
| Minimum latency | TBD | TBD |
| Average latency | TBD | TBD |
| Maximum latency | TBD | TBD |
| 95th percentile latency | TBD | TBD |

## Interpretation

### Execution Time

A lower execution time means the workload completed faster when the test conditions are comparable.

### Events per Second

Higher events per second indicates higher measured benchmark throughput.

### Average Latency

Lower average latency indicates that benchmark events took less time on average.

### 95th Percentile Latency

The 95th percentile shows the latency below which approximately 95% of measured events completed. It is useful for observing latency consistency.

## Observation

After collecting the two benchmark outputs, compare:

1. CPU throughput.
2. Total events completed.
3. Average latency.
4. Tail latency.
5. Total execution time.

The conclusion should be based only on the measured experiment.

## Limitations

- Results depend on the physical CPU and memory.
- Host background processes can affect Type-2 results.
- VM CPU scheduling can affect measurements.
- Storage configuration can affect system responsiveness.
- A single benchmark run is not sufficient to establish a universal hypervisor ranking.

For a stronger experiment, run each benchmark multiple times and report the mean and variation.
