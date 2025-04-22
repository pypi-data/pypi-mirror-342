"""
ccMonet MCP Server Configuration

This module contains configuration information for the ccMonet MCP server, such as API URL and authentication information.
"""
from typing import Dict, Any
import os

# API configuration
API_URL = "https://chatbot-prod.fly.dev/api/v3/chat"

# Get authentication information from environment variables, providing default values
ORG_ID = os.environ.get("CCMONET_ORG_ID")
AUTH_TOKEN = os.environ.get("CCMONET_AUTH_TOKEN")

# API request headers
API_HEADERS: Dict[str, Any] = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "x-org-id": ORG_ID,
    "Authorization": f"Bearer {AUTH_TOKEN}"
}

# Server configuration
SERVER_NAME = "ccMonet"

# Timeout settings (seconds)
REQUEST_TIMEOUT = 30.0 