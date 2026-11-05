# Experiment 5 – Kubernetes Resource Allocation, Scheduling & Load Balancing

## Aim
Analyze resource allocation, pod scheduling, and Service-based load balancing in an existing three-node Kubernetes cluster. The experiment deploys Nginx pods with CPU and memory requests/limits, monitors resource usage, scales replicas, and exposes the application through a NodePort Service.

## Environment
- Windows terminal with Docker Desktop / WSL2
- Kubernetes cluster created with `kind`
- Kubernetes version: `v1.37.0`
- Three nodes: `kind-control-plane`, `kind-worker`, and `kind-worker2`
- `kubectl`
- Nginx container image
- Metrics Server

## Files
| File | Description |
|---|---|
| `deployment.yaml` | Nginx Deployment with six replicas and CPU/memory requests and limits |
| `service.yaml` | NodePort Service exposing the Nginx pods on port 30080 |
| `observations.md` | Recorded outputs and observations from the practical |

## 1. Verify the cluster
```bash
kubectl get nodes -o wide
```
All three nodes should be in the `Ready` state.

## 2. Install and verify Metrics Server
Check whether Metrics Server is installed:
```bash
kubectl get deployment metrics-server -n kube-system
kubectl top nodes
```
If the Metrics API is unavailable, install Metrics Server:
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```
For this kind/WSL2 lab environment, the Metrics Server deployment required the `--kubelet-insecure-tls` argument. It was added by editing the deployment:
```bash
kubectl edit deployment metrics-server -n kube-system
```
Add `--kubelet-insecure-tls` under the container's `args`, save, and wait for the deployment to become ready:
```bash
kubectl get pods -n kube-system -l k8s-app=metrics-server
kubectl get apiservice v1beta1.metrics.k8s.io
kubectl top nodes
```
Use this TLS option only for this local learning cluster; it disables kubelet certificate verification and is not a production security configuration.

## 3. Deploy the Nginx application
Apply the deployment:
```bash
kubectl apply -f deployment.yaml
kubectl get pods -o wide
```
The Deployment initially requests six replicas. Each container requests 100m CPU and 64Mi memory, with limits of 200m CPU and 128Mi memory.

## 4. Inspect scheduling and resource allocation
```bash
kubectl get pods -o wide
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl describe nodes
kubectl top pods
kubectl top nodes
```
Use the `NODE` column to inspect placement. The node description reports capacity, allocatable resources, and requested/limited resources.

## 5. Scale the Deployment
Increase the replica count to twelve:
```bash
kubectl scale deployment resource-demo --replicas=12
kubectl get pods -o wide
kubectl top pods
```
Observe which pods become Running, Pending, or ContainerCreating and inspect scheduling events if a pod remains Pending.

## 6. Create and verify the NodePort Service
```bash
kubectl apply -f service.yaml
kubectl get services
kubectl get endpoints nginx-service
kubectl get endpointslices
```
The Service selects pods labelled `app: resource-demo` and exposes port 30080 on cluster nodes. In a kind environment, use port forwarding to access the application from the host:
```bash
kubectl port-forward svc/nginx-service 8080:80
```
Then open [http://127.0.0.1:8080](http://127.0.0.1:8080) in a browser. Keep the port-forward command running while testing.

## 7. Clean up
```bash
kubectl delete service nginx-service
kubectl delete deployment resource-demo
```
This removes the experiment's Service and Deployment. The existing kind cluster is not deleted.

## Results
- The three-node cluster was verified with all nodes in the `Ready` state.
- Metrics Server was configured successfully; `kubectl top nodes` and `kubectl top pods` returned CPU and memory metrics.
- The six-replica Nginx Deployment was created and its pods were scheduled across the two worker nodes.
- Scaling to twelve replicas created twelve desired pods. At the instant of the captured output, some additional pods were still Pending or ContainerCreating; this is recorded in `observations.md` rather than presented as twelve fully Running pods.
- The NodePort Service was created and its Endpoints/EndpointSlice showed backend pod addresses.
- The application was accessed from the host using `kubectl port-forward svc/nginx-service 8080:80`.
- The Service and Deployment were deleted after the test.

## Conclusion
The practical demonstrated Kubernetes resource requests and limits, scheduler placement across a multi-node cluster, scaling of a Deployment, monitoring through Metrics Server, and Service-based access to multiple Nginx pod endpoints. The captured run also showed that newly requested replicas may remain Pending temporarily while scheduling and container startup are in progress.

## Reference
Practical handout: *Kubernetes – Resource Allocation, Scheduling & Load Balancing*.
