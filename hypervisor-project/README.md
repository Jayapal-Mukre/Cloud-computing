# Type-1 vs Type-2 Hypervisor Performance Analysis

A Cloud Computing laboratory project comparing a **Type-1 hypervisor (Proxmox VE)** with a **Type-2 hypervisor (VMware Workstation)** using an Ubuntu virtual machine and the Sysbench CPU benchmark.

## Project Overview

This experiment studies how virtualization architecture can affect CPU performance.

### Hypervisors

- **Type-1:** Proxmox VE using KVM
- **Type-2:** VMware Workstation running on a host operating system

### Benchmark

```bash
sysbench cpu --cpu-max-prime=20000 run
```

The same guest operating system, virtual CPU allocation, memory allocation and benchmark configuration should be used for both environments as far as the available hardware permits.

## Objectives

1. Create an Ubuntu VM on Proxmox VE.
2. Create a comparable Ubuntu VM on VMware Workstation.
3. Verify CPU, memory and storage configuration.
4. Run the same Sysbench CPU workload in both VMs.
5. Record execution time, total events, throughput and latency.
6. Compare the measured results.
7. Document observations and limitations.

## Architecture

### Type-1 — Proxmox VE

```text
+-----------------------------+
|       Ubuntu VM             |
|    Sysbench CPU Test        |
+-----------------------------+
|      Proxmox VE / KVM       |
+-----------------------------+
|       Physical Hardware     |
+-----------------------------+
```

### Type-2 — VMware Workstation

```text
+-----------------------------+
|       Ubuntu VM             |
|    Sysbench CPU Test        |
+-----------------------------+
|    VMware Workstation       |
+-----------------------------+
|     Host Operating System   |
+-----------------------------+
|       Physical Hardware     |
+-----------------------------+
```

## Suggested VM Configuration

| Resource | Proxmox VE | VMware Workstation |
|---|---|---|
| Guest OS | Ubuntu | Ubuntu |
| vCPU | 2 | 2 |
| RAM | 2 GB | 2 GB |
| Disk | 20 GB | 20 GB |
| Benchmark | Sysbench CPU | Sysbench CPU |
| Prime limit | 20,000 | 20,000 |

Keep the configurations as similar as possible so that the comparison is meaningful.

## Experimental Procedure

### 1. Proxmox VE

- Create an Ubuntu VM.
- Allocate the agreed CPU, RAM and disk resources.
- Install Ubuntu.
- Verify the VM configuration.
- Install Sysbench.
- Run the benchmark.
- Save the terminal output and screenshots.

### 2. VMware Workstation

- Create a comparable Ubuntu VM.
- Allocate the same CPU, RAM and disk resources.
- Install Ubuntu.
- Verify the VM configuration.
- Install Sysbench.
- Run the same benchmark.
- Save the terminal output and screenshots.

### 3. Verify the Guest

Run:

```bash
lscpu
free -h
df -h /
```

### 4. Run the Benchmark

Install Sysbench:

```bash
sudo apt update
sudo apt install sysbench -y
```

Run:

```bash
sysbench cpu --cpu-max-prime=20000 run
```

Or use the supplied automation script:

```bash
chmod +x scripts/benchmark.sh
./scripts/benchmark.sh
```

## Project Structure

```text
hypervisor-project/
├── README.md
├── results/
│   └── performance-analysis.md
├── scripts/
│   ├── benchmark.sh
│   ├── parse_sysbench.py
│   └── generate_plots.py
└── screenshots/
    ├── comparison/
    ├── type1-proxmox/
    └── type2-vmware/
```

The screenshot directories are intentionally left for the screenshots from your own experiment. Do not present another student's measurements as your own.

## Result Recording

Record the actual output from both systems in `results/performance-analysis.md`.

Important metrics:

- Total execution time
- Total events
- Events per second
- Average latency
- Minimum latency
- Maximum latency
- 95th percentile latency, when reported by Sysbench

## Comparison

For throughput:

```text
Percentage improvement =
((Type-1 EPS - Type-2 EPS) / Type-2 EPS) × 100
```

For latency:

```text
Percentage reduction =
((Type-2 latency - Type-1 latency) / Type-2 latency) × 100
```

The result should be based on the actual benchmark output collected during the experiment.

## Important Note

Hypervisor performance depends on CPU model, host operating system, storage, memory pressure, VM configuration, virtualization extensions, background processes and benchmark conditions. Therefore, this project does **not** claim that one hypervisor is universally faster. It reports the observations from the controlled experiment.

## Technologies

- Proxmox VE
- KVM
- VMware Workstation
- Ubuntu
- Sysbench
- Bash
- Python
- Matplotlib

## Author

**Jayapal Mukre**

Cloud Computing Laboratory
