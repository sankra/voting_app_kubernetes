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

class AppDeploymentError(Exception):
    """
    Custom exception class for AppDeployment errors.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        logging.error(f"AppDeploymentError: {message}")


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