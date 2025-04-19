import requests
from typing import Optional, Dict

class Shadeform:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://novus-server-v3.fly.dev/api/v1/proxy/shadeform"
        # self.base_url = "http://103.54.57.253:8000/api/v1/proxy/shadeform"
        self.headers = {
            "apikey": self.api_key
        }

    def _request(self, method: str, endpoint: str, json: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Base request handler for Shadeform operations"""
        url = f"{self.base_url}/{endpoint}"
        
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=json,
            params=params
        )
        
        try:
            return response.json()
        except ValueError:
            return {
                "error": f"Failed to decode JSON response. Status code: {response.status_code}",
                "text": response.text
            }

    # Instance Management
    def create_instance(self, payload: Dict) -> Dict:
        """Launch a new GPU instance"""
        return self._request("POST", "instances/create", json=payload)

    def terminate_instance(self, instance_id: str) -> Dict:
        """Terminate a running instance"""
        return self._request("POST", "instances/terminate", json={"instance_id": instance_id})

    def list_instances(self) -> Dict:
        """List all instances"""
        return self._request("GET", "instances")
    
    def types_instances(self) -> Dict:
        """List available instance types"""
        return self._request("GET", "instances/types")

    def info_instance(self, instance_id: str) -> Dict:
        """Get details about a specific instance"""
        return self._request("GET", f"instances/{instance_id}/info")
    
    def update_instance(self, instance_id: str, payload: Dict) -> Dict:
        """Update instance settings"""
        return self._request("POST", f"instances/{instance_id}/update", json=payload)
    
    def restart_instance(self, instance_id: str) -> Dict:
        """Restart a running instance"""
        return self._request("POST", f"instances/{instance_id}/restart")

    def delete_instance(self, instance_id: str) -> Dict:
        """Delete an instance"""
        return self._request("POST", f"instances/{instance_id}/delete")

    # SSH Key Management
    def add_ssh_key(self, payload: Dict) -> Dict:
        """Register a new SSH key"""
        return self._request("POST", "sshkeys/add", json=payload)

    def list_ssh_keys(self) -> Dict:
        """List registered SSH keys"""
        return self._request("GET", "sshkeys")
    
    def ssh_key_info(self, key_id: str) -> Dict:
        """Get information about a specific SSH key"""
        return self._request("GET", f"sshkeys/{key_id}/info")
    
    def delete_ssh_key(self, key_id: str) -> Dict:
        """Delete a registered SSH key"""
        return self._request("POST", f"sshkeys/{key_id}/delete")

    def set_default_ssh_key(self, key_id: str) -> Dict:
        """Set a registered SSH key as default"""
        return self._request("POST", f"sshkeys/{key_id}/setdefault")

    # Storage Management
    def create_volume(self, payload: Dict) -> Dict:
        """Create persistent storage volume"""
        return self._request("POST", "volumes/create", json=payload)

    def info_volume(self, volume_id: str) -> Dict:
        """Get information about a specific storage volume"""
        return self._request("GET", f"volumes/{volume_id}/info")

    def delete_volume(self, volume_id: str) -> Dict:
        """Delete a storage volume"""
        return self._request("POST", f"volumes/{volume_id}/delete")
    
    def types_volume(self) -> Dict:
        """List available storage types"""
        return self._request("GET", "volumes/types")

    def list_volumes(self) -> Dict:
        """List all storage volumes"""
        return self._request("GET", "volumes")
    
    def list_templates(self) -> Dict:
        """List available templates"""
        return self._request("GET", "templates")

    def info_templates(self, template_id: str) -> Dict:
        """Get information about a specific template"""
        return self._request("GET", f"templates/{template_id}/info")
    
    def save_template(self, payload: Dict) -> Dict:
        """Save a template"""
        return self._request("POST", "templates/save", json=payload)
    
    def featured_templates(self) -> Dict:
        """List featured templates"""
        return self._request("GET", "templates/featured")
    
    def update_template(self, template_id: str, payload: Dict) -> Dict:
        """Update a template"""
        return self._request("POST", f"templates/{template_id}/update", json=payload)
    
    def delete_template(self, template_id: str) -> Dict:
        """Delete a template"""
        return self._request("POST", f"templates/{template_id}/delete")
