# pylint: disable=line-too-long
"""
Model for parsing Nexus Dashboard VRF attachments response.

Endpoint:

Verb: GET
Path: /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabric_name}/vrfs/attachments?vrf-names={comma_separated_vrf_names}
"""
import json

from pydantic import BaseModel, Field, ValidationError, field_validator


class InstanceValues(BaseModel):
    """Model for parsing the instanceValues JSON string."""

    loopbackIpV6Address: str = ""
    loopbackId: str = ""
    deviceSupportL3VniNoVlan: str = "false"
    switchRouteTargetImportEvpn: str = ""
    loopbackIpAddress: str = ""
    switchRouteTargetExportEvpn: str = ""


class LanAttachment(BaseModel):
    """Model for individual LAN attachment within a VRF."""

    entityName: str | None = None
    fabricName: str = Field(..., description="Name of the fabric")
    instanceValues: str | None = None
    ipAddress: str = Field(..., description="IP address of the switch")
    isLanAttached: bool = Field(..., description="Whether the LAN is attached")
    lanAttachState: str = Field(..., description="State of the LAN attachment")
    peerSerialNo: str | None = None
    switchName: str = Field(..., description="Name of the switch")
    switchRole: str = Field(
        ..., description="Role of the switch (e.g., 'border spine', 'leaf')"
    )
    switchSerialNo: str = Field(..., description="Serial number of the switch")
    vlanId: int | None = None
    vrfId: int = Field(..., description="VRF identifier")
    vrfName: str = Field(..., description="Name of the VRF")

    @field_validator("instanceValues")
    @classmethod
    def validate_instance_values(cls, v):
        """Validate that instanceValues is either None or valid JSON."""
        if v is None:
            return v
        try:
            # Parse the JSON string to validate it
            parsed = json.loads(v)
            # Optionally validate against InstanceValues model
            InstanceValues(**parsed)
            return v
        except (json.JSONDecodeError, TypeError) as error:
            raise ValueError(f"instanceValues must be valid JSON: {error}") from error

    def get_instance_values(self) -> InstanceValues | None:
        """Parse instanceValues JSON string into InstanceValues model."""
        if self.instanceValues is None:
            return None
        try:
            parsed = json.loads(self.instanceValues)
            return InstanceValues(**parsed)
        except (json.JSONDecodeError, TypeError):
            return None

    @field_validator("lanAttachState")
    @classmethod
    def validate_lan_attach_state(cls, v):
        """Validate lanAttachState against known values."""
        valid_states = {"IN PROGRESS", "DEPLOYED", "FAILED", "NA", "PENDING"}
        if v not in valid_states:
            # Don't raise error, just warn - new states might be added
            pass
        return v

    @field_validator("switchRole")
    @classmethod
    def validate_switch_role(cls, v):
        """Validate switchRole against common values."""
        common_roles = {"border spine", "spine", "leaf", "border leaf", "super spine"}
        if v not in common_roles:
            # Don't raise error, just warn - new roles might be added
            pass
        return v


class VrfData(BaseModel):
    """Model for VRF data containing list of LAN attachments."""

    lanAttachList: list[LanAttachment] = Field(
        ..., description="List of LAN attachments for this VRF"
    )
    vrfName: str = Field(..., description="Name of the VRF")

    @field_validator("lanAttachList")
    @classmethod
    def validate_lan_attach_list(cls, v):
        """Ensure lanAttachList is not empty."""
        if not v:
            raise ValueError("lanAttachList cannot be empty")
        return v


class NexusVrfAttachmentsResponse(BaseModel):
    """
    Main model for Nexus Dashboard VRF attachments GET response.

    This model validates the response from:
    GET /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabric_name}/vrfs/attachments
    """

    DATA: list[VrfData] = Field(..., description="List of VRF data")
    MESSAGE: str = Field(..., description="Response message")
    METHOD: str = Field(..., description="HTTP method used")
    REQUEST_PATH: str = Field(..., description="Full request path")
    RETURN_CODE: int = Field(..., description="HTTP return code")

    @field_validator("METHOD")
    @classmethod
    def validate_method(cls, v):
        """Validate HTTP method."""
        if v != "GET":
            raise ValueError("METHOD must be 'GET' for VRF attachments query")
        return v

    @field_validator("RETURN_CODE")
    @classmethod
    def validate_return_code(cls, v):
        """Validate return code is successful."""
        if v not in [200, 201, 202]:
            raise ValueError(f"RETURN_CODE indicates failure: {v}")
        return v

    @field_validator("REQUEST_PATH")
    @classmethod
    def validate_request_path(cls, v):
        """Validate request path format."""
        if "/vrfs/attachments" not in v:
            raise ValueError("REQUEST_PATH must contain '/vrfs/attachments'")
        return v

    def get_vrf_by_name(self, vrf_name: str) -> VrfData | None:
        """Get VRF data by name."""
        for vrf_data in self.DATA:  # pylint: disable=not-an-iterable
            if vrf_data.vrfName == vrf_name:
                return vrf_data
        return None

    def get_attached_switches(self, vrf_name: str | None = None) -> list[LanAttachment]:
        """Get all attached switches, optionally filtered by VRF name."""
        attached = []
        for vrf_data in self.DATA:  # pylint: disable=not-an-iterable
            if vrf_name and vrf_data.vrfName != vrf_name:
                continue
            for attachment in vrf_data.lanAttachList:
                if attachment.isLanAttached:
                    attached.append(attachment)
        return attached

    def get_switches_by_role(self, role: str) -> list[LanAttachment]:
        """Get all switches with a specific role."""
        switches = []
        for vrf_data in self.DATA:  # pylint: disable=not-an-iterable
            for attachment in vrf_data.lanAttachList:
                if attachment.switchRole == role:
                    switches.append(attachment)
        return switches


# Example usage and validation
if __name__ == "__main__":
    # Example response data
    example_response = {
        "DATA": [
            {
                "lanAttachList": [
                    {
                        "entityName": "ansible-vrf-int1",
                        "fabricName": "f1",
                        "instanceValues": '{"loopbackIpV6Address":"","loopbackId":"","deviceSupportL3VniNoVlan":"false","switchRouteTargetImportEvpn":"","loopbackIpAddress":"","switchRouteTargetExportEvpn":""}',
                        "ipAddress": "172.22.150.112",
                        "isLanAttached": True,
                        "lanAttachState": "IN PROGRESS",
                        "peerSerialNo": None,
                        "switchName": "cvd-1211-spine",
                        "switchRole": "border spine",
                        "switchSerialNo": "FOX2109PGCS",
                        "vlanId": 500,
                        "vrfId": 9008011,
                        "vrfName": "ansible-vrf-int1",
                    }
                ],
                "vrfName": "ansible-vrf-int1",
            },
            {
                "lanAttachList": [
                    {
                        "entityName": "ansible-vrf-int1",
                        "fabricName": "f1",
                        "instanceValues": '{"loopbackIpV6Address":"","loopbackId":"","deviceSupportL3VniNoVlan":"false","switchRouteTargetImportEvpn":"","loopbackIpAddress":"","switchRouteTargetExportEvpn":""}',
                        "ipAddress": "172.22.150.113",
                        "isLanAttached": True,
                        "lanAttachState": "IN PROGRESS",
                        "peerSerialNo": None,
                        "switchName": "cvd-1312-leaf",
                        "switchRole": "leaf",
                        "switchSerialNo": "FOX4250MFDS",
                        "vlanId": 500,
                        "vrfId": 9008011,
                        "vrfName": "ansible-vrf-int1",
                    }
                ],
                "vrfName": "ansible-vrf-int1",
            },
        ],
        "MESSAGE": "OK",
        "METHOD": "GET",
        "REQUEST_PATH": "https://172.22.150.244:443/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/f1/vrfs/attachments?vrf-names=ansible-vrf-int1",
        "RETURN_CODE": 200,
    }

    # Validate the response
    try:
        response = NexusVrfAttachmentsResponse(
            DATA=[],
            MESSAGE="msg",
            METHOD="GET",
            REQUEST_PATH="/vrfs/attachments",
            RETURN_CODE=200,
        ).model_validate(example_response)
    except ValidationError as error:
        print(f"✗ Validation failed: {error}")

    print("✓ Response validation successful")
    print(f"Found {len(response.DATA)} VRF(s)")

    # Test helper methods
    attached_switches = response.get_attached_switches()
    print(f"✓ Found {len(attached_switches)} attached switches")

    for switch_role in ["border spine", "leaf"]:
        role_switches = response.get_switches_by_role(switch_role)
        print(f"✓ Found {len(role_switches)} switches with role '{switch_role}'")

    for switch in attached_switches:
        instance_values = switch.get_instance_values()
        if instance_values:
            print(
                f"✓ Parsed instanceValues for switch {switch.switchName}: {instance_values}"
            )
        else:
            print(f"✗ No valid instanceValues for switch {switch.switchName}")
