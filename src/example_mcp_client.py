#!/usr/bin/env python3
"""
Example MCP (Model Context Protocol) Client Script

This script demonstrates how to create an MCP client using mcp.client.stdio
to connect to and interact with an MCP server.
"""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPClient:
    """
    A wrapper class for MCP client operations.
    
    This class provides high-level methods for interacting with an MCP server,
    including listing tools, calling tools, and managing resources.
    """
    
    def __init__(self, server_params: StdioServerParameters):
        self.server_params = server_params
        self.session: Optional[ClientSession] = None
    
    @asynccontextmanager
    async def connect(self):
        """
        Async context manager for connecting to the MCP server.
        
        Usage:
            async with client.connect() as session:
                # Use session here
                pass
        """
        async with stdio_client(self.server_params) as streams:
            stdin, stdout = streams
            async with ClientSession(stdin, stdout) as session:
                self.session = session
                try:
                    # Initialize the session
                    await session.initialize()
                    logger.info("Successfully connected to MCP server")
                    yield session
                finally:
                    self.session = None
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools from the MCP server.
        
        Returns:
            List of tool definitions
        """
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        try:
            result = await self.session.list_tools()
            tools = result.tools
            logger.info(f"Found {len(tools)} tools available")
            return [tool.model_dump() for tool in tools]
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            raise
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Call a specific tool with given arguments.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Dictionary of arguments to pass to the tool
        
        Returns:
            Tool execution result
        """
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        arguments = arguments or {}
        
        try:
            logger.info(f"Calling tool '{tool_name}' with arguments: {arguments}")
            result = await self.session.call_tool(tool_name, arguments)
            logger.info(f"Tool '{tool_name}' executed successfully")
            return {
                "content": [content.model_dump() for content in result.content],
                "isError": result.isError
            }
        except Exception as e:
            logger.error(f"Error calling tool '{tool_name}': {e}")
            raise
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """
        List all available resources from the MCP server.
        
        Returns:
            List of resource definitions
        """
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        try:
            result = await self.session.list_resources()
            resources = result.resources
            logger.info(f"Found {len(resources)} resources available")
            return [resource.model_dump() for resource in resources]
        except Exception as e:
            logger.error(f"Error listing resources: {e}")
            raise
    
    async def read_resource(self, resource_uri: str) -> Dict[str, Any]:
        """
        Read a specific resource by its URI.
        
        Args:
            resource_uri: URI of the resource to read
        
        Returns:
            Resource content
        """
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        try:
            logger.info(f"Reading resource: {resource_uri}")
            result = await self.session.read_resource(resource_uri)
            logger.info(f"Resource '{resource_uri}' read successfully")
            return {
                "contents": [content.model_dump() for content in result.contents]
            }
        except Exception as e:
            logger.error(f"Error reading resource '{resource_uri}': {e}")
            raise
    
    async def list_prompts(self) -> List[Dict[str, Any]]:
        """
        List all available prompts from the MCP server.
        
        Returns:
            List of prompt definitions
        """
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        try:
            result = await self.session.list_prompts()
            prompts = result.prompts
            logger.info(f"Found {len(prompts)} prompts available")
            return [prompt.model_dump() for prompt in prompts]
        except Exception as e:
            logger.error(f"Error listing prompts: {e}")
            raise
    
    async def get_prompt(self, prompt_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get a specific prompt with given arguments.
        
        Args:
            prompt_name: Name of the prompt to get
            arguments: Dictionary of arguments to pass to the prompt
        
        Returns:
            Prompt content
        """
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        arguments = arguments or {}
        
        try:
            logger.info(f"Getting prompt '{prompt_name}' with arguments: {arguments}")
            result = await self.session.get_prompt(prompt_name, arguments)
            logger.info(f"Prompt '{prompt_name}' retrieved successfully")
            return {
                "description": result.description,
                "messages": [message.model_dump() for message in result.messages]
            }
        except Exception as e:
            logger.error(f"Error getting prompt '{prompt_name}': {e}")
            raise


async def demonstrate_file_operations(client: MCPClient):
    """
    Demonstrate file operations using MCP tools.
    
    This assumes the server has file-related tools available.
    """
    print("\n=== File Operations Demo ===")
    
    try:
        # List files in current directory
        result = await client.call_tool("list_files", {"path": "."})
        print("Files in current directory:")
        for content in result["content"]:
            if content["type"] == "text":
                print(content["text"])
        
        # Create a test file
        test_content = "Hello from MCP client!\nThis is a test file."
        result = await client.call_tool("write_file", {
            "path": "mcp_test.txt",
            "content": test_content
        })
        print("\nCreated test file:")
        for content in result["content"]:
            if content["type"] == "text":
                print(content["text"])
        
        # Read the test file back
        result = await client.call_tool("read_file", {"path": "mcp_test.txt"})
        print("\nRead test file content:")
        for content in result["content"]:
            if content["type"] == "text":
                print(content["text"])
        
    except Exception as e:
        print(f"File operations demo failed: {e}")


async def demonstrate_web_search(client: MCPClient):
    """
    Demonstrate web search using MCP tools.
    
    This assumes the server has web search tools available.
    """
    print("\n=== Web Search Demo ===")
    
    try:
        # Perform a web search
        result = await client.call_tool("web_search", {
            "query": "MCP Model Context Protocol",
            "max_results": 3
        })
        print("Web search results:")
        for content in result["content"]:
            if content["type"] == "text":
                print(content["text"])
        
    except Exception as e:
        print(f"Web search demo failed: {e}")


async def demonstrate_resources(client: MCPClient):
    """
    Demonstrate resource operations.
    """
    print("\n=== Resources Demo ===")
    
    try:
        # List available resources
        resources = await client.list_resources()
        print("Available resources:")
        for resource in resources:
            print(f"  - {resource.get('name', 'Unknown')}: {resource.get('uri', 'No URI')}")
            if resource.get('description'):
                print(f"    Description: {resource['description']}")
        
        # Read a specific resource if available
        if resources:
            first_resource = resources[0]
            resource_uri = first_resource.get('uri')
            if resource_uri:
                content = await client.read_resource(resource_uri)
                print(f"\nContent of resource '{resource_uri}':")
                for item in content["contents"]:
                    if item["type"] == "text":
                        print(item["text"][:200] + "..." if len(item["text"]) > 200 else item["text"])
        
    except Exception as e:
        print(f"Resources demo failed: {e}")


async def demonstrate_prompts(client: MCPClient):
    """
    Demonstrate prompt operations.
    """
    print("\n=== Prompts Demo ===")
    
    try:
        # List available prompts
        prompts = await client.list_prompts()
        print("Available prompts:")
        for prompt in prompts:
            print(f"  - {prompt.get('name', 'Unknown')}")
            if prompt.get('description'):
                print(f"    Description: {prompt['description']}")
        
        # Get a specific prompt if available
        if prompts:
            first_prompt = prompts[0]
            prompt_name = first_prompt.get('name')
            if prompt_name:
                prompt_content = await client.get_prompt(prompt_name)
                print(f"\nPrompt '{prompt_name}':")
                print(f"Description: {prompt_content.get('description', 'No description')}")
                print("Messages:")
                for message in prompt_content["messages"]:
                    role = message.get('role', 'unknown')
                    content = message.get('content', {})
                    print(f"  {role}: {content}")
        
    except Exception as e:
        print(f"Prompts demo failed: {e}")


async def interactive_mode(client: MCPClient):
    """
    Interactive mode for manual tool testing.
    """
    print("\n=== Interactive Mode ===")
    print("Enter tool calls in the format: tool_name arg1=value1 arg2=value2")
    print("Type 'list' to see available tools")
    print("Type 'quit' to exit")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
            
            if user_input.lower() == 'list':
                tools = await client.list_tools()
                print("Available tools:")
                for tool in tools:
                    print(f"  - {tool.get('name', 'Unknown')}")
                    if tool.get('description'):
                        print(f"    Description: {tool['description']}")
                continue
            
            if not user_input:
                continue
            
            # Parse the input
            parts = user_input.split()
            tool_name = parts[0]
            
            arguments = {}
            for part in parts[1:]:
                if '=' in part:
                    key, value = part.split('=', 1)
                    # Try to convert to appropriate type
                    try:
                        # Try integer
                        value = int(value)
                    except ValueError:
                        try:
                            # Try float
                            value = float(value)
                        except ValueError:
                            # Keep as string, remove quotes if present
                            value = value.strip('"\'')
                    arguments[key] = value
            
            # Call the tool
            result = await client.call_tool(tool_name, arguments)
            print("Result:")
            for content in result["content"]:
                if content["type"] == "text":
                    print(content["text"])
                else:
                    print(f"[{content['type']}]: {content}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")


async def main():
    """
    Main function demonstrating various MCP client operations.
    """
    # Configure the MCP server parameters
    # Adjust these based on your MCP server setup
    server_params = StdioServerParameters(
        command="python",  # Command to run the MCP server
        args=["-m", "your_mcp_server_module"],  # Arguments for the server
        env=None  # Environment variables (optional)
    )
    
    # Alternative example for a Node.js server
    # server_params = StdioServerParameters(
    #     command="node",
    #     args=["path/to/your/server.js"],
    #     env={"NODE_ENV": "development"}
    # )
    
    # Create the client
    client = MCPClient(server_params)
    
    try:
        # Connect to the server and run demos
        async with client.connect() as session:
            print("Connected to MCP server successfully!")
            
            # List all available tools
            print("\n=== Available Tools ===")
            tools = await client.list_tools()
            for tool in tools:
                print(f"Tool: {tool.get('name', 'Unknown')}")
                if tool.get('description'):
                    print(f"  Description: {tool['description']}")
                if tool.get('inputSchema'):
                    print(f"  Input Schema: {tool['inputSchema']}")
                print()
            
            # Run various demonstrations
            await demonstrate_resources(client)
            await demonstrate_prompts(client)
            await demonstrate_file_operations(client)
            await demonstrate_web_search(client)
            
            # Enter interactive mode
            await interactive_mode(client)
    
    except Exception as e:
        logger.error(f"Error connecting to MCP server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Example of how to run with different server configurations
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Client Example")
    parser.add_argument("--command", default="python", help="Server command")
    parser.add_argument("--args", nargs="*", default=["-m", "your_mcp_server_module"], 
                       help="Server arguments")
    parser.add_argument("--interactive", action="store_true", 
                       help="Start in interactive mode only")
    
    args = parser.parse_args()
    
    # Update server parameters based on command line arguments
    server_params = StdioServerParameters(
        command=args.command,
        args=args.args,
        env=None
    )
    
    # Run the client
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient terminated by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)