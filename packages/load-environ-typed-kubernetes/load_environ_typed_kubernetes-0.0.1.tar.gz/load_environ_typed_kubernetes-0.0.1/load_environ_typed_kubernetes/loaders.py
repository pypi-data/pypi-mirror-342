from typing import Dict

import base64

import kubernetes.config  # type: ignore
import kubernetes.client  # type: ignore


class KubernetesLoader:
    """
    Class binding various loaders to help with access.

    Connecting to Kubernetes API requires credentials.

    This class supports either kube_config or in_cluster_config.

    kube_config is used during testing but also for applications
    that access the Kubernetes API from outside. It will read the
    context from ~/.kube/config or file pointed at by the
    $KUBECONFIG environment variable.

    in_cluster is used when running the pod inside a cluster. This
    requires a service account, role and rolebinding.

    This class instances its own Kubernetes API and client in order
    to not interfere with other Kubernetes clients you may be running.
    """
    def __init__(self, in_cluster: bool) -> None:
        configuration = kubernetes.client.Configuration()

        if in_cluster:
            kubernetes.config.load_incluster_config(client_configuration=configuration)
        else:
            kubernetes.config.load_kube_config(client_configuration=configuration)

        self.api_client = kubernetes.client.ApiClient(configuration=configuration)
        self.core_v1 = kubernetes.client.CoreV1Api(api_client=self.api_client)

    def load_config_map(self, raw: str) -> Dict[str, str]:
        """
        Loads the data from a ConfigMap.
        """
        if '.' in raw:
            namespace, name = raw.split('.', 1)
        else:
            namespace = 'default'
            name = raw

        config_map = self.core_v1.read_namespaced_config_map(name, namespace)
        return config_map.data  # type: ignore

    def load_config_map_binary(self, raw: str) -> Dict[str, bytes]:
        """
        Loads the binaryData from a ConfigMap.
        """
        if '.' in raw:
            namespace, name = raw.split('.', 1)
        else:
            namespace = 'default'
            name = raw

        config_map = self.core_v1.read_namespaced_config_map(name, namespace)
        return {
            k: base64.b64decode(v)
            for k, v in config_map.binary_data.items()
        }

    def load_secret(self, raw: str) -> Dict[str, str]:
        """
        Loads the data from a secret.

        This assumes all values can be decoded as UTF-8.
        """
        return {
            k: v.decode()
            for k, v in self.load_secret_binary(raw).items()
        }

    def load_secret_binary(self, raw: str) -> Dict[str, bytes]:
        """
        Loads the data from a secret.

        This assumes the values are binary data.
        """
        if '.' in raw:
            namespace, name = raw.split('.', 1)
        else:
            namespace = 'default'
            name = raw

        secret = self.core_v1.read_namespaced_secret(name, namespace)
        return {
            k: base64.b64decode(v)
            for k, v in secret.data.items()
        }
