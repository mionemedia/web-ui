"""Configuration for container communication."""

import os
from typing import Dict, Any

def get_backend_config() -> Dict[str, Any]:
    """
    Get the backend service configuration.
    
    Returns:
        Dict[str, Any]: Configuration dictionary with connection details
    """
    # Default to localhost if not running in containerized environment
    backend_host = os.environ.get('BACKEND_HOST', 'localhost')
    backend_port = int(os.environ.get('BACKEND_PORT', '9222'))
    
    return {
        'host': backend_host,
        'port': backend_port,
        'chrome_cdp_url': f"http://{backend_host}:{backend_port}",
        'ollama_endpoint': os.environ.get('OLLAMA_ENDPOINT', f"http://{backend_host}:11434"),
    }

def is_containerized() -> bool:
    """
    Check if running in a containerized environment.
    
    Returns:
        bool: True if running in a container, False otherwise
    """
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') or os.environ.get('BACKEND_HOST')
