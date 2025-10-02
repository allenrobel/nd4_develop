# pylint: disable=line-too-long
"""
A simple FastMCP server to provide developer resources for writing Ansible modules for ND 4.1
"""
import json
from pathlib import Path

from fastmcp import FastMCP
# from fastmcp import FastMCP
from fastmcp.resources import FileResource

def get_file_path(file_path: str) -> Path:
    """Get the absolute path of a file."""
    script_dir = Path(__file__).parent
    path = script_dir / file_path
    if path.exists():
        return path.resolve()
    raise ValueError(f"Path {path} does not exist")

def load_file(file_path: str) -> str:
    """Load a file and return its content"""
    path = get_file_path(file_path)
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return f.read()
    raise ValueError(f"Path {path.resolve()} does not exist")

def load_json_file(file_path: str) -> dict:
    """Load a JSON file and return its content as a dictionary."""
    return json.loads(load_file(file_path))


mcp: FastMCP = FastMCP(
    name="NexusDashboardDeveloperTools",
    instructions="""
    This server provides information that will be useful for developers
    working with the Nexus Dashboard REST API.  It includes tools for
    example payloads, links to Pydantic documentation, links to
    example Ansible playbooks, and more.
    """,
)

# VRF Payload Markdown Resource
# vrf_payload_md_path = Path("./payloads/v3/md/vrf.md").resolve()
vrf_payload_md_path = get_file_path("payloads/v3/md/vrf.md")
if vrf_payload_md_path.exists():
    vrf_payload_md_resource = FileResource(
        uri=f"file://{vrf_payload_md_path.as_posix()}",
        path=vrf_payload_md_path,
        name="VRF Payload Markdown",
        description="Markdown file that describes the VRF payload.",
        mime_type="text/markdown",
        tags={"documentation"},
    )
    mcp.add_resource(vrf_payload_md_resource)


# VRF Attachment Payload Markdown Resource
# vrf_attachment_payload_md_path = Path("./payloads/v3/md/vrf_attachment.md").resolve()
vrf_attachment_payload_md_path = get_file_path("payloads/v3/md/vrf_attachment.md")
if vrf_attachment_payload_md_path.exists():
    vrf_attachment_payload_md_resource = FileResource(
        uri=f"file://{vrf_attachment_payload_md_path.as_posix()}",
        path=vrf_attachment_payload_md_path,
        name="VRF Attachment Payload Markdown",
        description="Markdown file that describes the VRF attachment payload.",
        mime_type="text/markdown",
        tags={"documentation"},
    )
    mcp.add_resource(vrf_attachment_payload_md_resource)



# @mcp.prompt(
# name="ansible_developer_role",
# description="Loads and returns the Ansible developer role prompt from a specified file."
# )
# async def ansible_developer_role(file_path: str = "prompts/ansible_developer_role.json") -> dict:
#     """
#     Prompt that describes a Python developer writing an Ansible module.
#     Args:
#     file_path (str): Path to the prompt template file.
#     Returns:
#     str: The contents of the prompt file
#     """
#     return load_json_file(file_path)


@mcp.prompt(
name="ansible_developer_role",
description="Loads and returns the Ansible developer role prompt from a specified file."
)
async def ansible_developer_role(file_path: str = "prompts/ansible_developer_role.md") -> str:
    """
    Prompt that describes a Python developer writing an Ansible module.
    Args:
    file_path (str): Path to the prompt template file.
    Returns:
    str: The contents of the prompt file
    """
    return load_file(file_path)


@mcp.resource(
    uri="file:///resources/payloads/vrf.json",
    name="resource_nexus_dashboard_version_3_payload_vrf",
    description="Nexus Dashboard Version 3 VRF Payload Resource"
)
def resource_nexus_dashboard_version_3_payload_vrf() -> dict:
    """Nexus Dashboard Version 3 VRF Payload"""
    return load_json_file("./payloads/v3/vrf.json")

@mcp.tool(
    name="nexus_dashboard_version_3_payload_vrf",
    description="Nexus Dashboard Version 3 VRF Payload",
)
def nexus_dashboard_version_3_payload_vrf() -> dict:
    """Nexus Dashboard Version 3 VRF Payload"""
    return load_json_file("./payloads/v3/vrf.json")


@mcp.tool(name="nexus_dashboard_version_3_response_vrf_attachments")
def nexus_dashboard_version_3_response_vrf_attachments() -> dict:
    """
    Nexus Dashboard Version 3 VRF Attachments Response for the following endpoint:

    Path: /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/[fabric_name]/vrfs/attachments?vrf-names=[comma_separated_vrf_names]
    Verb: GET
    """
    return load_json_file("./responses/v3/vrf_attachments.json")


async def main():
    """Main function to run the FastMCP server."""
    print("In main()")
    await mcp.run_async(transport="stdio")


if __name__ == "__main__":
    print("Starting FastMCP server...")
    import asyncio

    asyncio.run(main())
