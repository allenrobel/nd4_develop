# VRF Payload

## Endpoint information

### Method

POST

### Path

/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{FABRIC_NAME}/vrfs

## Endpoint example usage

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-ndfc-token" \
  -d '{
    "fabric": "f1",
    "vrfName": "ansible-vrf-int1",
    "vrfId": 9008011,
    "vrfTemplate": "Default_VRF_Universal",
    "vrfTemplateConfig": "{\"vrfSegmentId\":9008011,\"vrfVlanId\":500,\"mtu\":9216}"
  }' \
  https://your-nexus-dashboard/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/f1/vrfs
```

## Field descriptions

### fabric

The name of the fabric in which the VRF resides.

type: str
min_length: 1
max_length: 64

### serviceVrfTemplate

A JSON string containing fields that define the configuration for
a service VRF associated with this VRF.

type: str

### source

Always null ???

### vrfExtensionTemplate

The name of a template that defines the configuration for VRF extension.

type: str
default: Default_VRF_Extension_Universal

### vrfId

The numerical ID of the VRF assigned by the controller, or the user.

type: int

### vrfName

The name of the VRF

type: str
min_length: 1
max_length: 32

### vrfTemplate

The name of a template that defines the configuration for this VRF.

type: str
default: Default_VRF_Universal

### vrfTemplateConfig

A JSON string consisting of the content of vrfTemplate.  This JSON string contains fields that define the configuration of the VRF.
