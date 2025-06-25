from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from os import path
import yaml

def cluster_connection():
    """Initialize and return Kubernetes CoreV1Api client."""
    config.load_kube_config()
    return client.CoreV1Api()

# Create a single API connection to reuse
api = cluster_connection()

def get_node_status(node_name):
    """Check node Ready status. Returns 'Ready' if so, None otherwise."""
    try:
        nodes = api.list_node().items
        for node in nodes:
            if node.metadata.name == node_name:
                for condition in node.status.conditions:
                    if condition.type == "Ready" and condition.status == "True":
                        return condition.type
    except ApiException as e:
        print(f"Error fetching node status: {e}")
    return None

def get_pods_in_namespace(namespace):
    """List all pod names in namespace."""
    try:
        pods = api.list_namespaced_pod(namespace).items
        return [p.metadata.name for p in pods]
    except ApiException as e:
        print(f"Error fetching pods in namespace '{namespace}': {e}")
        return []

def get_pod(namespace, podname):
    """Helper to fetch pod, or None if not found."""
    try:
        return api.read_namespaced_pod(podname, namespace)
    except ApiException as e:
        if e.status != 404:
            print(f"Pod '{podname}' not found: {e}")
        return None
        

def create_pod(namespace, podname):
    """
    Create a pod in the specified namespace from a YAML manifest if it does not exist.
    """
    pod = get_pod(namespace, podname)
    if pod is None:
        try:
            with open(path.join(path.dirname(__file__), "nginx-demo.yaml")) as f:
                body = yaml.safe_load(f)
                pod = api.create_namespaced_pod(namespace, body)
                print(f"Pod created with name '{pod.metadata.name}'")
                return pod.metadata.name
        except ApiException as e:
            print(f"Error Creating pod '{podname}': {e}")
            return None
    else:
        print(f"Pod '{podname}' already exists.")
        return pod.metadata.name


def get_pod_status(namespace, podname):
    """Return pod phase status, ('Running', 'Pending' ...)."""
    pod = get_pod(namespace, podname)
    return pod.status.phase if pod else None

def get_pod_readiness_status(namespace, podname):
    """Check pod readiness. Return 'Ready' if healthy, None otherwise."""
    pod = get_pod(namespace, podname)
    if pod:
        for condition in pod.status.conditions or []:
            if condition.type == "Ready" and condition.status == "True":
                return condition.type
    return None

def is_pod_having_probes(namespace, podname):
    """Return True if pod has liveness probe defined."""
    pod = get_pod(namespace, podname)
    if pod:
        for container in pod.spec.containers:
            if container.liveness_probe:
                return True
    return False

def check_pod_liveness_status(namespace, podname):
    """Check.
    Returns True if liveniess are good, otherwise False."""
    pod = cluster_connection().read_namespaced_pod(podname, namespace)
    # Check if all conatiners are running.
    is_pod_alive = True
    for con_sts in pod.status.container_statuses:
        if con_sts.ready != True:
            is_pod_alive = False 
    return is_pod_alive

def delete_pod(namespace, podname):
    """Delete pod if it exists."""
    pod = get_pod(namespace, podname)
    if pod:
        try:
            api.delete_namespaced_pod(
                name=podname,
                namespace=namespace,
                grace_period_seconds=0,
                body=client.V1DeleteOptions()
            )
            return True
        except ApiException as e:
            print(f"Error deleting pod '{podname}': {e}")
    return False


#print(get_node_status('ip-172-31-82-129'))
# print(get_pods_in_namespace("test-auto"))
create_pod("test-auto", "nginx-healthcheck")
# print(get_pod_readiness_status("test-auto", "nginx-healthcheck"))
# print(is_pod_having_probes("test-auto", "nginx-healthcheck"))
# print(check_pod_liveness_status("test-auto", "nginx-healthcheck"))
# print(delete_pod("test-auto", "nginx-healthcheck"))
