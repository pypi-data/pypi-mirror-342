from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic, Union, List  # Make sure to import the correct types
from datetime import datetime

T = TypeVar("T")

class DeviceLabel(BaseModel):
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    id: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None
    organization: Optional[str] = None


class Location(BaseModel):
    type: Optional[str] = None
    coordinates: Optional[List[Union[str, float]]] = None


class Site(BaseModel):
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    id: Optional[str] = None
    name: Optional[str] = None
    countryCode: Optional[str] = None
    timezone: Optional[str] = None
    address: Optional[str] = None
    location: Optional[Location] = None
    imageUrl: Optional[str] = None
    isDefault: Optional[bool] = None
    zoom: Optional[int] = None
    organization: Optional[str] = None


class Group(BaseModel):
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    provisioningTemplateName: Optional[str] = None
    isExtendScale: Optional[bool] = None
    site: Optional[str] = None


class FloorPlanImageCoordinates(BaseModel):
    type: Optional[str] = None
    coordinates: Optional[List[List[float]]] = None


class AreaGeometry(BaseModel):
    type: Optional[str] = None
    coordinates: Optional[List[List[List[float]]]] = None


class Floor(BaseModel):
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    id: Optional[str] = None
    name: Optional[str] = None
    floorNumber: Optional[int] = None
    floorPlanUrl: Optional[str] = None
    floorPlanImageCoordinates: Optional[FloorPlanImageCoordinates] = None
    relativeAltitude: Optional[float] = None
    areaGeometry: Optional[AreaGeometry] = None
    area: Optional[int] = None
    areaUnit: Optional[str] = None
    building: Optional[str] = None
    site: Optional[str] = None
    organization: Optional[str] = None


class Building(BaseModel):
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    id: Optional[str] = None
    name: Optional[str] = None
    site: Optional[str] = None
    organization: Optional[str] = None


class License(BaseModel):
    maxCount: Optional[int] = None
    currentCount: Optional[int] = None
    productId: Optional[str] = None
    expiredDate: Optional[str] = None
    gracePeriod: Optional[int] = None
    available: Optional[int] = None
    percentUsed: Optional[str] = None


class UpgradeSchedule(BaseModel):
    id: Optional[int] = None
    scheduleName: Optional[str] = None
    cronExpression: Optional[str] = None
    startDate: Optional[int] = None
    endDate: Optional[int] = None
    timeZone: Optional[str] = None
    duration: Optional[int] = None
    state: Optional[str] = None
    nextTriggerTime: Optional[int] = None
    prevTriggerTime: Optional[int] = None
    maxScope: Optional[str] = None
    orgId: Optional[str] = None


class Device(BaseModel):
    deviceLabels: Optional[List[DeviceLabel]] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    id: Optional[str] = None
    name: Optional[str] = None
    ipAddress: Optional[str] = None
    ipAddressV6: Optional[str] = None
    friendlyName: Optional[str] = None
    macAddress: Optional[str] = None
    serialNumber: Optional[str] = None
    deviceFamily: Optional[str] = None
    type: Optional[str] = ""
    physicalLocation: Optional[str] = ""
    description: Optional[str] = ""
    systemContact: Optional[str] = None
    location: Optional[str] = None
    floorElevation: Optional[int] = 0
    deviceStatus: Optional[str] = None
    currentSwVer: Optional[str] = None
    workingMode: Optional[str] = None
    lastSeenTime: Optional[int] = None
    imageLocation: Optional[str] = ""
    licenseStatus: Optional[str] = None
    autoChoosingLicenseMode: Optional[str] = None
    markPremium: Optional[bool] = None
    managementMode: Optional[str] = None
    isRap: Optional[bool] = None
    vpnSettingName: Optional[str] = None
    isAutoRegistered: Optional[bool] = None
    vcSerialNumber: Optional[str] = ""
    calculatedMacAddress: Optional[str] = None
    organization: Optional[str] = None
    site: Optional[Site] = None
    group: Optional[Group] = None
    building: Optional[Building] = None
    floor: Optional[Floor] = None
    license: Optional[License] = None
    lastEventReceivedAt: Optional[int] = None
    wiredPortLinkStatus: Optional[str] = ""
    vpnServers: Optional[List] = []
    iotStatus: Optional[str] = None
    ipMode: Optional[str] = None
    meshEnable: Optional[bool] = None
    meshRole: Optional[str] = ""
    meshIsRoot: Optional[bool] = None
    meshBand: Optional[str] = ""
    meshEssid: Optional[str] = ""
    meshPassphrase: Optional[str] = None
    ipv4Netmask: Optional[str] = None
    ipv4Gateway: Optional[str] = None
    ipv4DeviceDNS: Optional[str] = None
    ipv6Prefixlen: Optional[str] = ""
    ipv6Gateway: Optional[str] = None
    ipv6DeviceDNS: Optional[str] = None
    ledMode: Optional[str] = None
    lacpStatus: Optional[str] = None
    switchForQoeRtls: Optional[str] = None
    qoeSwitch: Optional[str] = None
    rtlsSwitch: Optional[str] = None
    flashThreshold: Optional[int] = None
    memoryThreshold: Optional[int] = None
    cpuThreshold: Optional[int] = None
    bleMac: Optional[str] = None
    iotPrivateSwitch: Optional[bool] = False
    iotMode: Optional[str] = None
    advertisingSwitch: Optional[bool] = False
    frequency: Optional[int] = None
    txPower: Optional[int] = None
    txChannel: Optional[List[int]] = []
    beaconMode: Optional[str] = None
    plainUrl: Optional[str] = ""
    nameSpace: Optional[str] = None
    instanceId: Optional[str] = None
    scanningSwitch: Optional[bool] = False
    scanningInterval: Optional[int] = None
    ouiWhiteList: Optional[List[str]] = []
    deviceCountryCode: Optional[str] = None
    apRadioConfigSwitch: Optional[str] = None
    band2: Optional[str] = None
    band5A: Optional[str] = None
    band5H: Optional[str] = None
    band5L: Optional[str] = None
    band6: Optional[str] = None
    _modifiedTS: Optional[datetime] = None
    callHomeInterval: Optional[int] = None
    chassisInfo: Optional[str] = None
    currentRunningDirectory: Optional[str] = None
    dataVpnServerIP: Optional[str] = None
    deviceFeatures: Optional[str] = None
    deviceLicenseMode: Optional[str] = ""
    deviceNaasMode: Optional[str] = None
    devicePrivateKey: Optional[str] = None
    devicePublicKey: Optional[str] = None
    deviceRole: Optional[str] = None
    deviceVpnIP: Optional[str] = None
    endIpAddress: Optional[str] = None
    ipAddressPoolOption: Optional[str] = None
    lengthIpAddress: Optional[str] = None
    manageRapVpnServer: Optional[str] = None
    manageRapVpnServerPort: Optional[int] = 0
    manageRapVpnServerPrivateKey: Optional[str] = None
    manageRapVpnServerPublicKey: Optional[str] = None
    networkIpAddress: Optional[str] = None
    ovEnterpriseServerIP: Optional[str] = None
    partNumber: Optional[str] = None
    pkiUpdateStatus: Optional[str] = None
    pkiUpdateTimestamp: Optional[str] = None
    rap: Optional[bool] = None
    startIpAddress: Optional[str] = None
    subnetMask: Optional[str] = None
    tcpMss: Optional[int] = None
    vcMacAddress: Optional[str] = ""
    upTime: Optional[int] = None
    bridgeApWebPassword: Optional[str] = None
    bridgeApWebSwitch: Optional[bool] = None
    bridgeDefault: Optional[str] = None
    bridgeFarEndApIp: Optional[str] = None
    bridgeFarEndApMac: Optional[str] = None
    bridgeSshPassword: Optional[str] = None
    bridgeSshSwitch: Optional[bool] = None
    bridgeWebCertName: Optional[str] = None
    lastRegisterEpochSecondTime: Optional[int] = None
    meshMode: Optional[str] = None
    meshParentNode: Optional[str] = ""
    channel: Optional[int] = None
    linkStatus: Optional[str] = None
    registrationStatus: Optional[str] = None
    registrationStatusReason: Optional[str] = None
    version: Optional[str] = None
    changes: Optional[str] = None
    apName: Optional[str] = None
    encryptionType: Optional[str] = None
    meshMcastRate: Optional[int] = None
    _insertedTS: Optional[datetime] = None
    activationStatus: Optional[str] = None
    currentRunningSoftwareVersion: Optional[str] = None
    lldpSwitch: Optional[bool] = None
    lastHeartBeat: Optional[int] = None
    modelName: Optional[str] = None
    licenseCategory: Optional[str] = None
    deviceLocation: Optional[str] = None
    workMode: Optional[str] = None
    managementConnectivity: Optional[str] = None
    numberOfLicensesUsed: Optional[int] = None
    rfProfile: Optional[str] = None
    upgradeSchedule: Optional[UpgradeSchedule] = None
    desiredSwVersion: Optional[str] = None
    scheduleLevel: Optional[str] = None
    rootMacFriendlyName: Optional[str] = None


class DeviceData(BaseModel):
    deviceLabels: Optional[List[DeviceLabel]] = []
    createdAt: Optional[str]
    updatedAt: Optional[str]
    id: Optional[str]
    name: Optional[str]
    ipAddress: Optional[str]
    ipAddressV6: Optional[str]
    friendlyName: Optional[str]
    macAddress: Optional[str]
    serialNumber: Optional[str]
    deviceFamily: Optional[str]
    type: Optional[str] = ""
    physicalLocation: Optional[str] = ""
    description: Optional[str] = ""
    systemContact: Optional[str]
    location: Optional[str]
    floorElevation: Optional[int] = 0
    deviceStatus: Optional[str]
    currentSwVer: Optional[str]
    workingMode: Optional[str]
    lastSeenTime: Optional[int]
    imageLocation: Optional[str] = ""
    licenseStatus: Optional[str]
    autoChoosingLicenseMode: Optional[str]
    markPremium: Optional[bool] = True
    managementMode: Optional[str]
    isRap: Optional[bool] = False
    vpnSettingName: Optional[str]
    isAutoRegistered: Optional[bool] = False
    vcSerialNumber: Optional[str] = ""
    calculatedMacAddress: Optional[str]
    organization: Optional[str]
    site: Optional[str]
    group: Optional[str]
    building: Optional[str]
    floor: Optional[str]
    license: Optional[License]
    iotStatus: Optional[str]
    ipMode: Optional[str]
    meshEnable: Optional[bool] = False
    meshRole: Optional[str] = ""
    meshIsRoot: Optional[bool] = False
    meshBand: Optional[str] = ""
    meshEssid: Optional[str] = ""
    meshPassphrase: Optional[str]
    ipv4Netmask: Optional[str]
    ipv4Gateway: Optional[str]
    ipv4DeviceDNS: Optional[str]
    ipv6Prefixlen: Optional[str] = ""
    ipv6Gateway: Optional[str]
    ipv6DeviceDNS: Optional[str]
    ledMode: Optional[str]
    lacpStatus: Optional[str]
    switchForQoeRtls: Optional[str]
    qoeSwitch: Optional[str]
    rtlsSwitch: Optional[str]
    flashThreshold: Optional[str]
    memoryThreshold: Optional[str]
    cpuThreshold: Optional[str]
    bleMac: Optional[str]
    iotPrivateSwitch: Optional[bool] = False
    iotMode: Optional[str]
    advertisingSwitch: Optional[bool] = False
    frequency: Optional[int] = 200
    txPower: Optional[int] = 4
    txChannel: Optional[List[int]] = []
    beaconMode: Optional[str]
    plainUrl: Optional[str] = ""
    nameSpace: Optional[str]
    instanceId: Optional[str]
    scanningSwitch: Optional[bool] = False
    scanningInterval: Optional[int] = 100
    ouiWhiteList: Optional[List[str]] = []
    deviceCountryCode: Optional[str]
    apRadioConfigSwitch: Optional[str]
    band2: Optional[str]
    band5A: Optional[str]
    band5H: Optional[str]
    band5L: Optional[str]
    band6: Optional[str]
    _modifiedTS: Optional[str]
    callHomeInterval: Optional[int]
    chassisInfo: Optional[str]
    currentRunningDirectory: Optional[str]
    dataVpnServerIP: Optional[str]
    deviceFeatures: Optional[str]
    deviceLicenseMode: Optional[str] = ""
    deviceNaasMode: Optional[str]
    devicePrivateKey: Optional[str]
    devicePublicKey: Optional[str]
    deviceRole: Optional[str]
    deviceVpnIP: Optional[str]
    endIpAddress: Optional[str]
    ipAddressPoolOption: Optional[str]
    lengthIpAddress: Optional[str]
    manageRapVpnServer: Optional[str]
    manageRapVpnServerPort: Optional[int] = 0
    manageRapVpnServerPrivateKey: Optional[str]
    manageRapVpnServerPublicKey: Optional[str]
    networkIpAddress: Optional[str]
    ovEnterpriseServerIP: Optional[str]
    partNumber: Optional[str]
    pkiUpdateStatus: Optional[str]
    pkiUpdateTimestamp: Optional[str]
    rap: Optional[bool] = False
    startIpAddress: Optional[str]
    subnetMask: Optional[str]
    tcpMss: Optional[int]
    vcMacAddress: Optional[str] = ""
    upTime: Optional[int]
    bridgeApWebPassword: Optional[str]
    bridgeApWebSwitch: Optional[str]
    bridgeDefault: Optional[str]
    bridgeFarEndApIp: Optional[str]
    bridgeFarEndApMac: Optional[str]
    bridgeSshPassword: Optional[str]
    bridgeSshSwitch: Optional[str]
    bridgeWebCertName: Optional[str]
    lastRegisterEpochSecondTime: Optional[int]
    meshMode: Optional[str]
    meshParentNode: Optional[str] = ""
    channel: Optional[int]
    linkStatus: Optional[str]
    registrationStatus: Optional[str]
    registrationStatusReason: Optional[str]
    version: Optional[str]
    changes: Optional[str]
    apName: Optional[str]
    encryptionType: Optional[str]
    meshMcastRate: Optional[str]
    _insertedTS: Optional[str]
    activationStatus: Optional[str]
    currentRunningSoftwareVersion: Optional[str]
    lldpSwitch: Optional[bool] = True
    lastHeartBeat: Optional[int]
    modelName: Optional[str]
    licenseCategory: Optional[str]
    deviceLocation: Optional[str]
    workMode: Optional[str]
    lastEventReceivedAt: Optional[int]
    managementConnectivity: Optional[str]
    provisioningTemplate: Optional[str]
    valueMappingTemplate: Optional[str]
    mgmtUsersTemplate: Optional[str]
    saveAndCertify: Optional[bool] = True
    provisioningResultState: Optional[str]
    rfProfile: Optional[str]
    upgradeSchedule: Optional[UpgradeSchedule]
    desiredSwVersion: Optional[str]
    scheduleLevel: Optional[str]
    rootMacFriendlyName: Optional[str]    
   
class SaveToRunningResponse(BaseModel):
    devicesIds: Optional[List[str]] = []
    macAddresses: Optional[List[str]] = []

class RebootResponse(BaseModel):
    macAddresses: Optional[List[str]] = []  


class Error(BaseModel):
    type: Optional[str] = None
    field: Optional[str] = None
    errorMsg: Optional[str] = None 


class DeviceResponse(BaseModel, Generic[T]):  # Inherit directly from BaseModel
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[T] = None
    errorCode: Optional[int] = None
    errorMsg: Optional[str] = None
    errorDetailsCode: Optional[str] = None
    errorDetails: Optional[Union[str, dict]] = None  # Accept both str and dict
    errors: Optional[List[Error]] = None      
