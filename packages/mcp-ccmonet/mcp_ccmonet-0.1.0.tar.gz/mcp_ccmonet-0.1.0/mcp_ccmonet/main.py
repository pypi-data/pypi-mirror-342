#!/usr/bin/env python
"""
ccMonet MCP Server Entry Point

Run this file to start the MCP server for interacting with clients like Claude.
"""
from mcp_ccmonet.ccmonet_server.server import mcp


def main():
    """MCP server entry point function"""
    print("Starting ccMonet MCP server...")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main() 