# Import local functions
from k8s_api_func import (
    cluster_connection,
    get_node_status,
    create_pod,
    get_pods_in_namespace,
    get_pod_status,
    is_pod_having_probes,
    get_pod_readiness_status,
    check_pod_liveness_status,
    delete_pod
)

# Constants to use globaly
TEST_NAMESPACE = "test-auto"
EMPTY_NAMESPACE = "empty-ns"
TEST_POD = "nginx-healthcheck"
TEST_NODE = "ip-172-31-82-248"
DEFAULT_NAMESPACE = "default"

def test_cluster_connection():
    """Test that cluster connection lists namespaces."""
    namespaces = cluster_connection().list_namespace(timeout_seconds=5)
    assert namespaces.items is not None, "Cluster connection failed"

def test_node_status():
    """Test that a specific node is Ready."""
    assert get_node_status(TEST_NODE) == "Ready", f"Node {TEST_NODE} is not Ready"

def test_getting_pods_in_namespace():
    """Test that a non-empty namespace returns pods."""
    pods = get_pods_in_namespace(TEST_NAMESPACE)
    assert len(pods) > 0, f"No pods found in namespace {TEST_NAMESPACE}"

def test_getting_pods_in_empty_namespace():
    """Test that an empty namespace returns empty pod list."""
    pods = get_pods_in_namespace(EMPTY_NAMESPACE)
    assert len(pods) == 0, f"Expected no pods in {EMPTY_NAMESPACE}, found {len(pods)}"

def test_getting_correct_pod_status():
    """Test that a known pod is Running."""
    assert get_pod_status(TEST_NAMESPACE, TEST_POD) == "Running", f"{TEST_POD} is not Running"

def test_getting_incorrect_pod_status():
    """Test that a pod is not Running."""
    assert get_pod_status(DEFAULT_NAMESPACE, TEST_POD) != "Running", f"{TEST_POD} unexpectedly Running in {DEFAULT_NAMESPACE}"

def test_pod_probes_check():
    """Test that the pod has liveness probes."""
    assert is_pod_having_probes(TEST_NAMESPACE, TEST_POD), f"{TEST_POD} does not have liveness probes"

def test_pod_readiness_status():
    """Test that the pod reports Ready."""
    assert get_pod_readiness_status(TEST_NAMESPACE, TEST_POD) == "Ready", f"{TEST_POD} is not Ready"

def test_pod_liveness_status():
    """Test that the pod is live (all containers ready)."""
    assert check_pod_liveness_status(TEST_NAMESPACE, TEST_POD), f"{TEST_POD} liveness check failed"

def test_pod_deletion_success():
    """Test that the pod deletion succeeds."""
    assert delete_pod(TEST_NAMESPACE, TEST_POD), f"{TEST_POD} deletion failed"
