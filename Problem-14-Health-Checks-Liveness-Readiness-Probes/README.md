# Problem 14: Health Checks Using Liveness and Readiness Probes

## Aim
To deploy a containerized web application on Kubernetes and demonstrate health monitoring using **liveness** and **readiness** probes.

## Tools and Technologies
- Docker
- Kubernetes
- Kind (Kubernetes IN Docker)
- kubectl
- Python 3.12
- Flask

## Experiment Overview
A small Flask application exposes HTTP endpoints used by Kubernetes probes. The application is packaged into a Docker image and deployed with two replicas in the `probe-lab` namespace. A Kubernetes Service routes traffic only to ready pods.

### Application endpoints

| Endpoint | Purpose | Healthy response |
|---|---|---|
| `/` | Application information | HTTP 200 |
| `/live` | Liveness probe endpoint | `{"status":"Alive"}` |
| `/ready` | Readiness probe endpoint | `{"status":"Ready"}` |
| `/fail-liveness` | Simulate liveness failure | Sets liveness state to failed |
| `/fail-readiness` | Simulate readiness failure | Sets readiness state to failed |
| `/recover` | Restore both health states | Resets both flags |

## Project Structure

```text
Problem-14-Health-Checks-Liveness-Readiness-Probes/
├── app.py
├── requirements.txt
├── Dockerfile
├── deployment.yaml
├── service.yaml
└── README.md
```

## Implementation

### 1. Build the Docker image

Run these commands from the folder containing the Dockerfile:

```bash
docker build -t health-probe-demo:v1 .
kind load docker-image health-probe-demo:v1
```

### 2. Create namespace and deploy

```bash
kubectl create namespace probe-lab
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

If the namespace already exists, continue without recreating it.

### 3. Verify deployment

```bash
kubectl get nodes
kubectl get deployments -n probe-lab
kubectl get pods -n probe-lab -o wide
kubectl get services -n probe-lab
```

Expected: Deployment reports 2/2 available replicas and both pods become 1/1 Ready.

### 4. Access the application

In one terminal:

```bash
kubectl port-forward service/health-probe-service 8081:80 -n probe-lab
```

In another terminal:

```bash
curl http://127.0.0.1:8081/
curl http://127.0.0.1:8081/live
curl http://127.0.0.1:8081/ready
```

On Windows Command Prompt, use `curl.exe` if needed.

## Demonstration: Readiness Probe

Use a port-forward to target one pod directly (replace the pod name if it changes):

```bash
kubectl get pods -n probe-lab
kubectl port-forward pod/<pod-name> 8082:8080 -n probe-lab
```

In another terminal, simulate failure and inspect pod readiness and Service endpoints:

```bash
curl http://127.0.0.1:8082/fail-readiness
kubectl get pods -n probe-lab
kubectl get endpoints health-probe-service -n probe-lab
```

Expected observation:
- The affected pod becomes `0/1` Ready but remains Running.
- Its restart count does not increase.
- Its IP is removed from the Service endpoints.
- The other healthy replica remains available.

Recover the pod:

```bash
curl http://127.0.0.1:8082/recover
kubectl get pods -n probe-lab
kubectl get endpoints health-probe-service -n probe-lab
```

After the readiness check succeeds, the pod is added back to the Service endpoints.

## Demonstration: Liveness Probe

With the same pod-specific port-forward active:

```bash
curl http://127.0.0.1:8082/fail-liveness
kubectl get pods -n probe-lab -w
```

Wait for Kubernetes to detect repeated liveness failures. Press Ctrl+C to stop watching, then run:

```bash
kubectl get pods -n probe-lab
kubectl describe pod <pod-name> -n probe-lab
```

Expected observation:
- The container is restarted after the liveness failure threshold is reached.
- The pod's restart count increases.
- The application starts with its default healthy in-memory flags and becomes Ready again.

## Probe Configuration

| Setting | Liveness | Readiness |
|---|---:|---:|
| HTTP path | `/live` | `/ready` |
| Port | 8080 | 8080 |
| Initial delay | 5 seconds | 3 seconds |
| Period | 5 seconds | 3 seconds |
| Timeout | 2 seconds | 2 seconds |
| Failure threshold | 3 | 2 |

## Result and Observations

The experiment demonstrated both health checks:
1. **Readiness failure:** Kubernetes marked the affected pod unready and removed it from Service endpoints without restarting the container.
2. **Readiness recovery:** The pod became Ready again and returned to the Service endpoints.
3. **Liveness failure:** Kubernetes restarted the unhealthy container after consecutive failed checks.
4. **Liveness recovery:** The restarted application became healthy and Ready again.

## Conclusion

Kubernetes liveness and readiness probes were successfully demonstrated using a Flask application deployed as two replicas in a Kind cluster. The readiness probe controlled whether a pod received Service traffic, while the liveness probe detected an unhealthy container and triggered its restart. This verified Kubernetes health monitoring and automatic container recovery.

## Important Notes
- The failure flags are process-local in-memory variables. A container restart resets them to their healthy defaults.
- Use a pod-specific port-forward when testing failures so that the request reaches the intended replica rather than an arbitrary Service backend.
- A Kind NodePort Service is not necessarily reachable directly from the host unless the Kind cluster was configured with port mappings. Port-forwarding is used here for reliable local access.
- The `kubectl get endpoints` command may show a deprecation warning on recent Kubernetes versions; EndpointSlices are the newer API.
