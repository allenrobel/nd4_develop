# VRF Attachments Payload

## Endpoint information

### Method

POST

### Path

/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{FABRIC_NAME}/vrfs/attachments

## Endpoint example usage

```bash
curl -X POST \
  "https://192.168.1.100/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/MyFabric/vrfs/attachments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "vrfName": "Tenant-1",
    "lanAttachList": [
      {
        "fabric": "MyFabric",
        "vrfName": "Tenant-1",
        "serialNumber": "FDO211218GC",
        "vlan": 100,
        "deployment": true,
        "extensionTemplate": "Default_VRF_Extension_Universal",
        "instanceValues": {
          "loopbackId": "",
          "loopbackIpAddress": "",
          "loopbackIpV6Address": ""
        }
      }
    ]
  }'
```

## Path Field Descriptions

### FABRIC_NAME

The name of the fabric in which the VRF resides.

type: str
min_length: 1
max_length: 64

## Payload Field descriptions

### vrfName

The name of the VRF

type: str
min_length: 1
max_length: 32

### lanAttachList

A list (array) of objects (dict) with fields describing an attachment.

#### lanAttachList.fabric

The name of the fabric in which the VRF resides.

type: str
min_length: 1
max_length: 64

### lanAttachList.vrfName

The name of the VRF

type: str
min_length: 1
max_length: 32

### lanAttachList.serialNumber

The serial number of the switch on which the attachment will be configured.

type: str
min_length: 1

### lanAttachList.vlan

The vlan with which the VRF attachment is associated.

type: int
min: 2
max: 4094

### lanAttachList.deployment

Controls whether the attachment is to be created or deleted.

If true, the attachment is to be created.
If false, the attachment is to be deleted.

type: bool

### lanAttachList.extensionTemplate

The name of a template that defines VRF extension parameters for this VRF.
This describes a VRF Lite configuration.

type: str
default: Default_VRF_Extension_Universal

### lanAttachList.instanceValues

A JSON string consisting of configuration parameters for the attachment.

type: str

#### lanAttachList.instanceValues.loopbackId

The Loopback interface ID associated with this attachment.

For example interface loopback5, the ID is 5.

type: int
min: 0
max: 1023

Example: loopback10

#### lanAttachList.instanceValues.loopbackIpAddress

The IPv4 address of the loopback interface, in CIDR format.

type: str

Example: 192.168.1.10/32

#### lanAttachList.instanceValues.loopbackIpV6Address

The IPv6 address of the loopback interface, in CIDR format.

type: str

Example: 2001::1/128
