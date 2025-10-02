# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastMCP (Model Context Protocol) demo project that implements a simple MCP server that provides
information useful for developing Ansible modules for Nexus Dashboard. The project uses the FastMCP
library to create an MCP server that can be used by Claude or other AI assistants.

## Key Files

- `mcp_server.py`: Contains tools that return information about Nexus Dashboard
  payloads, controller responses, Ansible playbooks, etc, use for Ansible
  module development.
- `pyproject.toml`: Project configuration using uv for dependency management

## Common Commands

### Development

```bash
# Install dependencies
uv sync

# Run the MCP server
python mcp_server.py
```

### MCP Server Usage

The server exposes tools that can be called by MCP clients:

- `nexus_dashboard_version_3_response_vrf_attachments()`: Return a Nexus Dashboard response for the VRF attachments endpoint.
- `nexus_dashboard_version_3_vrf_payload()`: Returns an example payload to create a VRF.

## Architecture Notes

- Uses FastMCP framework for MCP server implementation
- Simple tool-based architecture where functions are decorated with `@mcp.tool`
- Server runs on standard MCP protocol when executed directly
