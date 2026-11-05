# Experiment 5 – Observations

## Cluster
The cluster contained three Ready nodes:
- `kind-control-plane` – Kubernetes v1.37.0
- `kind-worker` – Kubernetes v1.37.0
- `kind-worker2` – Kubernetes v1.37.0

The cluster ran on Debian GNU/Linux 13 nodes under WSL2 with containerd.

## Metrics Server
Initially, `kubectl top nodes` returned `Metrics API not available`, and the Metrics Server Deployment was absent. Metrics Server was installed from the Kubernetes SIGs release manifest. The local kind/WSL2 setup needed the `--kubelet-insecure-tls` argument. After editing the Deployment and waiting for it to become ready, the APIService reported `AVAILABLE=True` and `kubectl top nodes` returned metrics.

One captured node sample:
| Node | CPU | CPU % | Memory | Memory % |
|---|---:|---:|---:|---:|
| kind-control-plane | 364m | 9% | 571Mi | 14% |
| kind-worker | 104m | 2% | 228Mi | 5% |
| kind-worker2 | 128m | 3% | 272Mi | 7% |

A later sample after the Service test:
| Node | CPU | CPU % | Memory | Memory % |
|---|---:|---:|---:|---:|
| kind-control-plane | 430m | 10% | 582Mi | 15% |
| kind-worker | 173m | 4% | 302Mi | 7% |
| kind-worker2 | 220m | 5% | 343Mi | 8% |

## Six-replica Deployment
The Deployment created six Nginx pods. In the captured node description, three pods were allocated to `kind-worker` and three to `kind-worker2`. Each pod had a CPU request of 100m, CPU limit of 200m, memory request of 64Mi, and memory limit of 128Mi.

Captured `kubectl top pods` output showed approximately 4Mi memory per Nginx pod and very low CPU use (mostly 0m at the sample time).

## Scaling to twelve replicas
The Deployment was scaled with:
```bash
kubectl scale deployment resource-demo --replicas=12
```
The desired replica count became twelve. At the moment the pod list was captured, six existing pods were Running and the newly created pods were still in Pending or ContainerCreating states. This is a time-specific snapshot, not proof that the additional pods could never be scheduled.

## Service and application access
The `nginx-service` NodePort Service was created with port mapping `80:30080/TCP`. The Endpoints output listed multiple pod IP addresses, and the EndpointSlice listed the Service's backend addresses.

The direct URL placeholder was mistakenly entered as a command in the terminal. The application was then accessed successfully using:
```bash
kubectl port-forward svc/nginx-service 8080:80
```
The terminal reported forwarding on `127.0.0.1:8080` and handled browser connections.

## Cleanup
Both resources were deleted:
```bash
kubectl delete service nginx-service
kubectl delete deployment resource-demo
```
