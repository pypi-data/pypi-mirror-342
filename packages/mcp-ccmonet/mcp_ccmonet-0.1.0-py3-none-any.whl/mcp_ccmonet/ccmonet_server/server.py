"""
ccMonet MCP Server

This server uses the Model Context Protocol to interact with clients such as the Claude desktop application,
and forwards user messages to the specified API.
"""
from typing import Any, Dict
import httpx
from mcp.server.fastmcp import FastMCP

# Import configuration
from mcp_ccmonet.ccmonet_server.config import (
    API_URL, 
    API_HEADERS, 
    SERVER_NAME, 
    REQUEST_TIMEOUT
)

# Initialize FastMCP server
mcp = FastMCP(SERVER_NAME)


async def make_api_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Send a request to the API and return the response

    Args:
        payload: The request body to send

    Returns:
        The API response content
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                API_URL,
                headers=API_HEADERS,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # In a production application, you might want better error handling
            return {"error": f"API request failed: {str(e)}"}


@mcp.tool()
async def send_message(message: str) -> str:
    """Consult with Monet about the company's financial status

    As CFO, Monet is responsible for:
    - Monitoring the company's financial health
    - Analyzing financial data and trends to guide business decisions
    - Managing the company's financial risks
    - Ensuring compliance with financial regulations and accounting standards (such as GAAP, IFRS)
    - Providing financial perspective for the company's strategic planning
    - Optimizing the company's capital structure and investment portfolio
    - Leading budget planning and financial forecasting
    - Evaluating the financial feasibility of business expansion, acquisitions, or investment opportunities

    Args:
        message: Financial questions to ask Monet

    Returns:
        Professional financial advice from Monet
    """
    payload = {
        "message": message,
        "thread_id": None,
        "response_message_id": None
    }
    
    # Send API request
    response = await make_api_request(payload)
    
    # Process API response
    if "error" in response:
        return f"Error: {response['error']}"
    
    # Return message content
    if "message" in response:
        return response['message']
    
    # If the response structure doesn't match expectations, return the entire response
    return str(response)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio') 