# Lab Evaluation Report: Containerized Microservice Application
## Domain: Gym Management System

---

## 1. Executive Summary & Aim
**Aim:** To develop a microservice-based application containing three independent services, containerize and deploy the services using Docker, establish inter-service communication, generate varying workloads, monitor resource utilization, and analyze application performance.

---

## 2. Microservice Architecture & Design (Checkpoint 1 - 1 Mark)

### Architecture Diagram
```
                           +------------------------+
                           |     Client / User      |
                           +-----------+------------+
                                       |
                                       v  HTTP REST
                           +------------------------+
                           |   Attendance Service   |
                           |       (Port 8003)      |
                           +---+----------------+---+
                               |                |
                     HTTP REST |                | HTTP REST
                               v                v
                 +-------------------+    +-----------------------+
                 |   Member Service  |    |   Membership Service  |
                 |    (Port 8001)    |    |      (Port 8002)      |
                 +-------------------+    +-----------------------+
```

### Microservice Responsibilities & REST APIs

| Service Name | Responsibility | Port | Primary REST API Endpoints |
|---|---|---|---|
| **Member Service** | Manages gym member profiles (Creation, Retrieval, Updates, Deletions). | 8001 | `GET /members`<br>`POST /members`<br>`GET /members/{id}`<br>`PUT /members/{id}`<br>`DELETE /members/{id}` |
| **Membership Service** | Manages subscription plans (Gold, VIP, Start/End Dates, Active/Expired Status). | 8002 | `GET /memberships`<br>`POST /memberships`<br>`GET /memberships/{member_id}`<br>`PUT /memberships/{member_id}` |
| **Attendance Service** | Coordinates member check-ins and check-outs by verifying member identity and subscription status across services. | 8003 | `GET /attendance/{member_id}`<br>`POST /attendance/checkin?member_id={id}`<br>`POST /attendance/checkout/{attendance_id}` |

---

## 3. Containerization & Deployment (Checkpoint 2 - 1 Mark)

Each microservice is containerized using `python:3.11-slim` with dedicated `Dockerfile` specifications and deployed onto a unified Docker network via `docker-compose.yml`.

### Docker Compose Architecture
- **Network:** `gym-network` (bridge driver for inter-container communication)
- **Volumes:** `member-db`, `membership-db`, `attendance-db` (persistent volume mounts mapped to `/app/data/`)

```yaml
services:
  member-service:
    build: ./member-service
    container_name: gym-member-service
    ports:
      - "8001:8000"
    volumes:
      - member-db:/app/data
    networks:
      - gym-network

  membership-service:
    build: ./membership-service
    container_name: gym-membership-service
    ports:
      - "8002:8000"
    volumes:
      - membership-db:/app/data
    networks:
      - gym-network

  attendance-service:
    build: ./attendance-service
    container_name: gym-attendance-service
    ports:
      - "8003:8000"
    environment:
      - MEMBER_SERVICE_URL=http://member-service:8000
      - MEMBERSHIP_SERVICE_URL=http://membership-service:8000
    volumes:
      - attendance-db:/app/data
    networks:
      - gym-network
    depends_on:
      - member-service
      - membership-service
```

---

## 4. Inter-Service Communication Proof (Checkpoint 3 - 1 Mark)

### Sequence Flow for End-to-End Check-In Request
1. Client sends `POST /attendance/checkin?member_id=1` to **Attendance Service** (`gym-attendance-service:8003`).
2. **Attendance Service** makes an internal asynchronous HTTP call to `http://member-service:8000/members/1` to verify member existence.
3. **Attendance Service** makes an internal asynchronous HTTP call to `http://membership-service:8000/memberships/1` to verify active subscription status (`status == 'ACTIVE'`).
4. If verified, **Attendance Service** records timestamped attendance entry (`PRESENT`) in SQLite and returns composite JSON response.

```json
{
  "message": "Check-in successful",
  "attendance_id": 1,
  "member_id": 1,
  "member_name": "Alice Smith",
  "membership_plan": "VIP_GOLD",
  "membership_status": "ACTIVE",
  "status": "PRESENT",
  "check_in": "2026-10-07 22:50:40"
}
```

---

## 5. Workload Testing & Performance Monitoring (Checkpoint 4 - 1 Mark)

Workload generation was executed using `workload_test.py` across 5 concurrency levels ($W_1$ to $W_5$). Real-time resource metrics were collected from container stats (`docker stats`).

### Observation Table

| Workload Level | Concurrency (Concurrent Requests) | Total Requests | Successful Requests | Failed Requests | Average Response Time (ms) | Throughput (req/sec) | Attendance Service Mem (MB) | Member Service Mem (MB) | Membership Service Mem (MB) |
|---|---|---|---|---|---|---|---|---|---|
| **W1** | 1 | 30 | 30 | 0 | **10.14 ms** | **98.38 req/s** | 60.94 MB | 52.48 MB | 52.43 MB |
| **W2** | 2 | 40 | 40 | 0 | **15.52 ms** | **126.71 req/s** | 66.38 MB | 52.70 MB | 52.91 MB |
| **W3** | 4 | 50 | 50 | 0 | **27.40 ms** | **142.50 req/s** | 67.85 MB | 52.93 MB | 52.90 MB |
| **W4** | 8 | 60 | 60 | 0 | **54.78 ms** | **142.29 req/s** | 85.40 MB | 53.18 MB | 53.14 MB |
| **W5** | 16 | 80 | 80 | 0 | **101.24 ms** | **150.50 req/s** | 90.53 MB | 56.65 MB | 55.61 MB |

---

## 6. Performance Analysis & Results Presentation (Checkpoint 5 - 1 Mark)

### Recommended Visual Performance Charts

````carousel
![Response Time Chart](/Users/sammedpatil/.gemini/antigravity/brain/b7d2cc85-c91b-48c7-baf4-b0f96d16dc22/chart_response_time.png)
<!-- slide -->
![Throughput Chart](/Users/sammedpatil/.gemini/antigravity/brain/b7d2cc85-c91b-48c7-baf4-b0f96d16dc22/chart_throughput.png)
<!-- slide -->
![CPU Utilization Chart](/Users/sammedpatil/.gemini/antigravity/brain/b7d2cc85-c91b-48c7-baf4-b0f96d16dc22/chart_cpu_utilization.png)
<!-- slide -->
![Memory Utilization Chart](/Users/sammedpatil/.gemini/antigravity/brain/b7d2cc85-c91b-48c7-baf4-b0f96d16dc22/chart_memory_utilization.png)
````

### Key Findings & Deep-Dive Analysis
1. **Response Time Trend:** As concurrent requests scale from $1$ to $16$, average response time increases from $10.14\text{ ms}$ to $101.24\text{ ms}$ linearly. This occurs because worker threads queue incoming HTTP requests and SQLite database locking occurs during concurrent check-in writes.
2. **Throughput Saturation:** Throughput scales rapidly from $98.38\text{ req/s}$ ($W_1$) to $142.50\text{ req/s}$ ($W_3$), before stabilizing around $150.50\text{ req/s}$ ($W_5$). This indicates optimal resource saturation point around $8\text{--}16$ concurrency.
3. **Resource Consumption Distribution:** The **Attendance Service** consumes significantly more memory ($90.53\text{ MB}$) compared to Member Service ($56.65\text{ MB}$) and Membership Service ($55.61\text{ MB}$).
   - **Reason:** The Attendance Service manages downstream HTTP connection pools (`httpx.AsyncClient`) to both microservices simultaneously, maintaining async request contexts for each inbound transaction.
4. **Reliability:** Zero request failures ($0\%$) were recorded across all test levels under varying concurrent loads.

---

## 7. Evaluator Presentation Q&A Guide

> [!TIP]
> **Q1: Why did you choose 3 microservices instead of a monolithic structure?**
> **A:** Decoupling Member management, Membership subscriptions, and Attendance tracking enables independent deployment, scaling, and fault tolerance. For instance, high attendance check-in load does not degrade member profile lookups.

> [!TIP]
> **Q2: How do containers communicate inside Docker?**
> **A:** Containers are attached to a custom bridge network (`gym-network`). Docker's embedded DNS resolves container service names (e.g. `http://member-service:8000`) directly to container IP addresses.

> [!TIP]
> **Q3: Which service is the bottleneck under high load and why?**
> **A:** The Attendance Service is the primary resource consumer because it acts as an orchestrator, handling dual outbound HTTP connections per incoming request while managing concurrent database transactions.

---

## 8. Conclusion
The Gym Management containerized microservice application successfully fulfills all requirements across Checkpoints 1 through 5. Inter-service communication via Docker DNS bridge network was verified, workload benchmarks demonstrated predictable performance scaling, and resource utilization was quantitatively measured and analyzed.
