"""
Deployment configuration for HackRx API
This file contains configuration for different deployment platforms
"""

import os
from typing import Dict, Any

# Base configuration
BASE_CONFIG = {
    "host": "0.0.0.0",
    "port": int(os.getenv("PORT", 8000)),
    "workers": int(os.getenv("WEB_CONCURRENCY", 1)),
    "timeout": 120,
    "keepalive": 5,
}

# Platform-specific configurations
PLATFORM_CONFIGS = {
    "heroku": {
        "bind": f"{BASE_CONFIG['host']}:{BASE_CONFIG['port']}",
        "workers": BASE_CONFIG["workers"],
        "timeout": BASE_CONFIG["timeout"],
        "keepalive": BASE_CONFIG["keepalive"],
        "worker_class": "uvicorn.workers.UvicornWorker",
        "preload_app": True,
    },
    "railway": {
        "bind": f"{BASE_CONFIG['host']}:{BASE_CONFIG['port']}",
        "workers": BASE_CONFIG["workers"],
        "timeout": BASE_CONFIG["timeout"],
        "keepalive": BASE_CONFIG["keepalive"],
        "worker_class": "uvicorn.workers.UvicornWorker",
        "preload_app": True,
    },
    "render": {
        "bind": f"{BASE_CONFIG['host']}:{BASE_CONFIG['port']}",
        "workers": BASE_CONFIG["workers"],
        "timeout": BASE_CONFIG["timeout"],
        "keepalive": BASE_CONFIG["keepalive"],
        "worker_class": "uvicorn.workers.UvicornWorker",
        "preload_app": True,
    },
    "local": {
        "host": "127.0.0.1",
        "port": 8000,
        "reload": True,
        "log_level": "info",
    }
}

def get_config(platform: str = None) -> Dict[str, Any]:
    """Get configuration for specified platform"""
    if not platform:
        platform = os.getenv("DEPLOYMENT_PLATFORM", "local")
    
    return PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["local"])

def get_gunicorn_config(platform: str = None) -> str:
    """Generate gunicorn configuration string"""
    config = get_config(platform)
    
    if platform == "local":
        return ""
    
    config_str = ""
    for key, value in config.items():
        if isinstance(value, str):
            config_str += f"{key} = '{value}'\n"
        else:
            config_str += f"{key} = {value}\n"
    
    return config_str

if __name__ == "__main__":
    # Print configuration for current platform
    platform = os.getenv("DEPLOYMENT_PLATFORM", "local")
    print(f"Configuration for platform: {platform}")
    print(get_config(platform))
