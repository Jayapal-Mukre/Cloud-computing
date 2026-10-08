# Smart College Event Microservices Platform

A containerized microservice application for managing college events, registrations, and notifications.

## Features
- Python FastAPI
- Docker and Docker Compose
- Separate SQLite database per service
- REST API communication
- Automated API testing
- Concurrent workload benchmarking
- Matplotlib performance graphs

## Services

| Service | Port | Responsibility |
|---|---:|---|
| Event Service | 8001 | Create and manage college events |
| Registration Service | 8002 | Register students and validate events |
| Notification Service | 8003 | Store registration notifications |

## Architecture

College Dashboard -> Event Service
College Dashboard -> Registration Service
College Dashboard -> Notification Service

Registration Service -> Event Service
Registration Service -> Notification Service

Each service owns its own SQLite database.

## Run

From the microservice-project directory:

    docker compose up --build

Open:
- http://localhost:8001/docs
- http://localhost:8002/docs
- http://localhost:8003/docs
- dashboard/index.html

Stop:

    docker compose down

## Test

With the containers running:

    pip install requests matplotlib
    python run_tests.py

## Benchmark

Run:

    python workload_test.py

Concurrency levels: 1, 10, 25, 50 and 100.

Metrics:
- Average latency
- Throughput
- Error rate
- Successful requests
- Failed requests

Generate graphs:

    python generate_graphs.py

## Project Structure

    microservice-project/
    ├── event-service/
    ├── registration-service/
    ├── notification-service/
    ├── dashboard/
    ├── docker-compose.yml
    ├── run_tests.py
    ├── workload_test.py
    ├── generate_graphs.py
    ├── benchmark_results.json
    └── LAB_REPORT.md

## Important
Benchmark values are templates until the experiment is actually executed. No unexecuted measurements are presented as real results.

## Learning Outcomes
1. Understand microservice decomposition.
2. Containerize independent services.
3. Use Docker Compose for multi-container deployment.
4. Implement REST-based inter-service communication.
5. Measure latency and throughput under increasing workloads.
6. Analyze performance bottlenecks.