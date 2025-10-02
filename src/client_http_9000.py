import asyncio
import json
from fastmcp.client import Client

async def test_client():
    """Call the 'example_nexus_dashboard_version_3_vrf_payload' tool."""
    client = Client("http://localhost:9000/mcp")
    try:
        async with client:
            await client.ping()
            prompt_result = await client.get_prompt_mcp("ansible_developer_role")
            print(prompt_result)

            tool_result = await client.call_tool("nexus_dashboard_version_3_payload_vrf")
            #tool_result = json.loads(tool_result.data)
            print(tool_result)
            # print(json.dumps(tool_result, indent=4, sort_keys=True))

            # tool_result = await client.call_tool("nexus_dashboard_version_3_response_vrf_attachments")
            # tool_result = json.loads(tool_result.data)
            # print(json.dumps(tool_result, indent=4, sort_keys=True))

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("--- Client Interaction Finished ---")

if __name__ == "__main__":
    asyncio.run(test_client())
