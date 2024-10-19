from k8s_manager import KubernetesNamespaceManager


manager = KubernetesNamespaceManager()

# 1. Create namespace
manager.create_namespace("test-namespace")

# 2. Allocate resource quota to the namespace
manager.allocate_resource_quota("test-namespace", memory_limit="4Gi", cpu_limit="2", storage_limit="10Gi", gpu_limit=None)

# 3. Optionally, delete the namespace
# manager.delete_namespace("test-namespace")
