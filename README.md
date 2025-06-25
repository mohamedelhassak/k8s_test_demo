
# Kubernetes API Tests

## ⚙ Requirements

- Python 3.x
- Install dependencies:
  ```bash
  pip install kubernetes pyyaml
  ```
- Access to a Kubernetes cluster (`~/.kube/config`)

## Kubernetes API Utility

This module provides a set of Python functions to interact with a Kubernetes cluster  
using the official Kubernetes Python client.


### Features

- Connect to a Kubernetes cluster
- Check node readiness status
- List pod names in a namespace
- Get pod phase (e.g. Running, Pending)
- Check pod readiness condition
- Check if pod has liveness probes
- Verify container liveness
- Create pod from YAML manifest
- Delete pod safely

### Functions

| Function | Purpose |
|-----------|---------|
| `cluster_connection()` | Initialize API client |
| `get_node_status()` | Check node is Ready |
| `get_pods_in_namespace()` | List pods in namespace |
| `get_pod()` | Get pod object |
| `create_pod()` | Create pod from YAML |
| `get_pod_status()` | Get pod phase |
| `get_pod_readiness_status()` | Check pod readiness |
| `is_pod_having_probes()` | Check liveness probe |
| `check_pod_liveness_status()` | Verify containers ready |
| `delete_pod()` | Delete pod |

### Example

```python
create_pod("test-auto", "nginx-healthcheck")
print(get_node_status(NODE_NAME))
```

### Notes

- The `nginx-demo.yaml` file must exist in the same directory.


## Kubernetes Tests

This module provides a **Python test functions** using the Kubernetes Python client  
to validate the state of Kubernetes cluster resources, such as nodes and pods.

### Features

- Verify cluster connection and list namespaces  
- Check node readiness (`Ready` state)  
- Validate pod listing in namespaces  
- Check pod phase (e.g., `Running`)  
- Ensure pod readiness and liveness  
- Confirm pod has liveness probes  
- Create and delete pods safely  

### Test Functions

| Function | What it tests |
|-----------|---------------|
| `test_cluster_connection()` | Cluster connection works |
| `test_node_status()` | Node is Ready |
| `test_getting_pods_in_namespace()` | Namespace has pods |
| `test_getting_pods_in_empty_namespace()` | Empty namespace returns no pods |
| `test_getting_correct_pod_status()` | Pod is Running |
| `test_getting_incorrect_pod_status()` | Pod not Running in wrong ns |
| `test_pod_probes_check()` | Pod has liveness probes |
| `test_pod_readiness_status()` | Pod reports Ready |
| `test_pod_liveness_status()` | Pod containers ready |
| `test_pod_deletion_success()` | Pod deletion succeeds |

### Run Tests

```bash
pytest k8s_api_tests.py -v
```