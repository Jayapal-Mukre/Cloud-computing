# Cloud Computing Microservice Lab Report

## Title
Smart College Event Microservices Platform: Containerization and Workload Analysis

## Objective
Design, deploy, test and analyze a multi-container microservice application using FastAPI, Docker and Docker Compose.

## Problem Statement
College event management combines event creation, student registration and notifications. This project separates these responsibilities into independently deployable services and studies application behavior as request concurrency increases.

## Experiment
Deploy the application with Docker Compose. Send 200 requests at concurrency levels 1, 10, 25, 50 and 100.

## Metrics
- Average latency
- Throughput
- Error rate
- Successful requests
- Failed requests

## Results
Run the workload experiment first. Then use the actual values from benchmark_results.json in the final report.

## Observations
Record how latency changes with concurrency, whether throughput reaches saturation, and whether errors appear at higher loads.

## Conclusion
The experiment demonstrates independent service deployment, REST-based service communication, container orchestration with Docker Compose and empirical workload analysis.
