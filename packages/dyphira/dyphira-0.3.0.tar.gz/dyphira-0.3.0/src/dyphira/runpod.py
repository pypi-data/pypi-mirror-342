
import requests
import os
import json

class RunPod:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://novus-server-v3.fly.dev/api/v1/proxy/runpod"
        # self.base_url = "http://103.54.57.253:8000/api/v1/proxy/runpod"
        self.headers = {
            "Content-Type": "application/json",
            "apikey": f"{self.api_key}"
        }

    def _request(self, method, endpoint, params=None, data=None, files=None):
        """Make a request to the RunPod API."""
        url = f"{self.base_url}/{endpoint}"
        
        if data and not files:
            data = json.dumps(data)
            
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            data=data,
            files=files
        )
        
        if response.status_code >= 400:
            raise Exception(f"Error {response.status_code}: {response.text}")
            
        return response.json()

    # Pod management
    def get_pods(self):
        """Get all pods for the authenticated user."""
        return self._request("GET", "pods")
        
    def get_pod(self, pod_id):
        """Get details for a specific pod."""
        return self._request("GET", f"pods/{pod_id}")
        
    def create_pod(self, pod_config):
        """Create a new pod with the specified configuration.
        
        Args:
            pod_config: Dict containing pod configuration as per PodCreateInput schema
        """
        return self._request("POST", "pods", data=pod_config)
        
    def update_pod(self, pod_id, pod_config):
        """Update an existing pod with new configuration.
        
        Args:
            pod_id: ID of the pod to update
            pod_config: Dict containing pod configuration as per PodUpdateInput schema
        """
        return self._request("PUT", f"pods/{pod_id}", data=pod_config)
        
    def delete_pod(self, pod_id):
        """Delete/terminate a pod."""
        return self._request("DELETE", f"pods/{pod_id}")
        
    def start_pod(self, pod_id):
        """Start a stopped pod."""
        return self._request("POST", f"pods/{pod_id}/start")
        
    def stop_pod(self, pod_id):
        """Stop a running pod."""
        return self._request("POST", f"pods/{pod_id}/stop")

    # Serverless endpoints
    def get_endpoints(self):
        """Get all serverless endpoints for the authenticated user."""
        return self._request("GET", "endpoints")
        
    def get_endpoint(self, endpoint_id):
        """Get details for a specific serverless endpoint."""
        return self._request("GET", f"endpoints/{endpoint_id}")
        
    def create_endpoint(self, endpoint_config):
        """Create a new serverless endpoint.
        
        Args:
            endpoint_config: Dict containing endpoint configuration
        """
        return self._request("POST", "endpoints", data=endpoint_config)
        
    def update_endpoint(self, endpoint_id, endpoint_config):
        """Update an existing serverless endpoint."""
        return self._request("PUT", f"endpoints/{endpoint_id}", data=endpoint_config)
        
    def delete_endpoint(self, endpoint_id):
        """Delete a serverless endpoint."""
        return self._request("DELETE", f"endpoints/{endpoint_id}")

    # Network volumes
    def get_network_volumes(self):
        """Get all network volumes for the authenticated user."""
        return self._request("GET", "networkvolumes")
        
    def get_network_volume(self, volume_id):
        """Get details for a specific network volume."""
        return self._request("GET", f"networkvolumes/{volume_id}")
        
    def create_network_volume(self, volume_config):
        """Create a new network volume."""
        return self._request("POST", "networkvolumes", data=volume_config)
        
    def delete_network_volume(self, volume_id):
        """Delete a network volume."""
        return self._request("DELETE", f"networkvolumes/{volume_id}")

    # Templates
    def get_templates(self):
        """Get all templates for the authenticated user."""
        return self._request("GET", "templates")
        
    def get_template(self, template_id):
        """Get details for a specific template."""
        return self._request("GET", f"templates/{template_id}")

