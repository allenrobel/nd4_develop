"""
Test environment settings for FastMCP.
This script demonstrates how to access and modify global settings in FastMCP.
"""
from fastmcp.settings import Settings

settings = Settings()

for item in settings:
    print(f"{item[0]}: {item[1]}")
