from kubernetes import client, config
from kubernetes.client.rest import ApiException


class KubernetesNamespaceManager:
    def __init__(self, kube_config_path=None):
        # Initialize Kubernetes client and store it as an attribute
        if kube_config_path:
            config.load_kube_config(config_file=kube_config_path)
        else:
            config.load_kube_config()  # Loads default kube config path
        self.client = client  # Encapsulate the kubernetes client here
        self.core_api = self.client.CoreV1Api()

    def create_namespace(self, namespace_name) -> client.V1Namespace:
        """
        Create a namespace in the Kubernetes cluster.
        """
        namespace = self.client.V1Namespace(
            metadata=self.client.V1ObjectMeta(name=namespace_name)
        )
        try:
            self.core_api.create_namespace(namespace)
            print(f"Namespace '{namespace_name}' created successfully.")
        except ApiException as e:
            if e.status == 409:
                print(f"Namespace '{namespace_name}' already exists.")
            else:
                print(f"Exception creating namespace: {e}")
        return namespace
    
    def allocate_resource_quota(self, namespace_name, memory_limit, cpu_limit, storage_limit, gpu_limit=None) -> client.V1ResourceQuota:
        """
        Assign resource quota to an existing namespace.
        """
        # Define resource quota limits
        hard_limits = {
            "requests.cpu": cpu_limit,
            "requests.memory": memory_limit,
            "requests.storage": storage_limit,
            "limits.cpu": cpu_limit,
            "limits.memory": memory_limit,
        }

        # Add GPU limits if provided
        if gpu_limit:
            hard_limits["requests.nvidia.com/gpu"] = gpu_limit
            hard_limits["limits.nvidia.com/gpu"] = gpu_limit

        # Create a resource quota object
        resource_quota = self.client.V1ResourceQuota(
            metadata=self.client.V1ObjectMeta(name=f"{namespace_name}-quota"),
            spec=self.client.V1ResourceQuotaSpec(hard=hard_limits)
        )

        try:
            self.core_api.create_namespaced_resource_quota(namespace_name, resource_quota)
            print(f"Resource quota for namespace '{namespace_name}' created successfully.")
        except ApiException as e:
            print(f"Exception creating resource quota: {e}")
        return resource_quota

    def create_pod_in_namespace(self, namespace_name, pod_name, image_name, container_port=None):
        """
        Create a pod in the given namespace using the specified image name.
        """
        # Define container spec
        container = self.client.V1Container(
            name=pod_name,
            image=image_name,
            ports=[self.client.V1ContainerPort(container_port=container_port)] if container_port else []
        )

        # Define pod spec
        pod_spec = self.client.V1PodSpec(containers=[container])

        # Define pod metadata and specification
        pod = self.client.V1Pod(
            metadata=self.client.V1ObjectMeta(name=pod_name),
            spec=pod_spec
        )

        try:
            self.core_api.create_namespaced_pod(namespace=namespace_name, body=pod)
            print(f"Pod '{pod_name}' created successfully in namespace '{namespace_name}'.")
        except ApiException as e:
            print(f"Exception creating pod '{pod_name}': {e}")

    def delete_namespace(self, namespace_name):
        """
        Delete a namespace from the Kubernetes cluster.
        """
        try:
            self.core_api.delete_namespace(name=namespace_name)
            print(f"Namespace '{namespace_name}' deleted successfully.")
        except ApiException as e:
            print(f"Exception deleting namespace: {e}")
