import kubernetes
import logging
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import List, Dict, Any

class AppDeployment:
    def __init__(self, kube_config_path: str):
        """
        Initialize the AppDeployment class with the path to the Kubernetes config file.
        """
        self.kube_config_path = kube_config_path
        self.api_client = None
        self.apps_v1 = None
        self.core_v1 = None
        self._initialize_kubernetes_client()

    def _initialize_kubernetes_client(self):
        """
        Initialize the Kubernetes client using the provided config file.
        """
        try:
            config.load_kube_config(config_file=self.kube_config_path)
            self.api_client = client.ApiClient()
            self.apps_v1 = client.AppsV1Api(self.api_client)
            self.core_v1 = client.CoreV1Api(self.api_client)
            logging.info("Kubernetes client initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Kubernetes client: {e}")
            raise


class AppDeploymentStatus:
    """
    Class to manage the status of the AppDeployment.
    """
    def __init__(self, deployment_name: str, namespace: str):
        self.deployment_name = deployment_name
        self.namespace = namespace

    def get_status(self) -> Dict[str, Any]:
        try:
            api_response = self.apps_v1.read_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace
            )
            return api_response.status.to_dict()
        except ApiException as e:
            logging.error(f"Failed to get deployment status: {e}")
            raise

class AppDeploymentError(Exception):
    """
    Custom exception class for AppDeployment errors.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        logging.error(f"AppDeploymentError: {message}")

    def __str__(self):
        return f"AppDeploymentError: {self.message}"

class AppDeploymentConfig:
    """
    Class to manage the configuration of the AppDeployment.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def get_config(self) -> Dict[str, Any]:
        """
        Get the deployment configuration.
        """
        return self.config

    def set_config(self, config: Dict[str, Any]):
        """
        Set the deployment configuration.
        """
        self.config = config
        logging.info("Deployment configuration updated.")

class AppDeploymentManager(AppDeployment):
    """Class to manage the deployment of applications in Kubernetes.
    This class extends the AppDeployment class and provides methods to create, update, and delete deployments.
    """    

    def create_deployment(self, namespace: str, deployment_config: Dict[str, Any]):
        """s
        Create a deployment in the specified namespace.
        """
        try:
            api_response = self.apps_v1.create_namespaced_deployment(
                body=deployment_config,
                namespace=namespace
            )
            logging.info(f"Deployment created: {api_response.metadata.name}")
            return api_response
        except ApiException as e:
            raise AppDeploymentError(f"Failed to create deployment: {e}")


def main():
    """
    Main function to demonstrate the usage of the AppDeployment class.
    """
    kube_config_path = "path/to/kubeconfig"  # Replace with your kubeconfig path
    app_deployment = AppDeployment(kube_config_path)

    # Example usage: List all deployments in a namespace
    namespace = "default"
    try:
        deployments = app_deployment.apps_v1.list_namespaced_deployment(namespace)
        for deployment in deployments.items:
            print(f"Deployment Name: {deployment.metadata.name}")
            print(f"Namespace: {deployment.metadata.namespace}")
    except ApiException as e:
        logging.error(f"Exception when listing deployments: {e}")
    # Example usage: Create a deployment
    deployment_config = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "example-deployment",
            "namespace": namespace
        },
        "spec": {
            "replicas": 2,
            "selector": {
                "matchLabels": {
                    "app": "example-app"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "example-app"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "example-container",
                            "image": "nginx:latest"
                        }
                    ]
                }
            }
        }
    }