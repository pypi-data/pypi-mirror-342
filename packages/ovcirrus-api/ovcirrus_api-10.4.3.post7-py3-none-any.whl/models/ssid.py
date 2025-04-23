from typing import Optional, TypeVar, Generic, Union, List, Dict, Any  # Make sure to import the correct types
from pydantic import BaseModel

T = TypeVar("T")

class CaptivePortal(BaseModel):
    captivePortalType: Optional[str] = "NONE"
    httpsRedirection: Optional[bool] = False


class ClientSessionLogging(BaseModel):
    clientSessionLoggingStatus: Optional[bool] = False
    loggingLevel: Optional[str] = "NONE"


class WalledGarden(BaseModel):
    allowDomains: Optional[List[str]] = []
    socialLoginVendor: Optional[List[str]] = []


class AccessRoleProfile(BaseModel):
    arpName: Optional[str] = ""
    bandwidthControl: Optional[Dict[str, Any]] = {}
    captivePortal: Optional[CaptivePortal] = CaptivePortal()
    childStatus: Optional[bool] = False
    clientIsolationAllowedList: Optional[List[str]] = []
    clientSessionLogging: Optional[ClientSessionLogging] = ClientSessionLogging()
    dhcpOption82Status: Optional[bool] = False
    id: Optional[int] = 0
    saveAsDistinct: Optional[bool] = False
    useExistingAclAndQos: Optional[bool] = True
    useExistingLocationPolicy: Optional[bool] = True
    useExistingPeriodPolicy: Optional[bool] = True
    useExistingPolicyList: Optional[bool] = False
    walledGarden: Optional[WalledGarden] = WalledGarden()


class AuthenticationStrategy(BaseModel):
    aaaProfileId: Optional[int] = 0
    byPassStatus: Optional[bool] = False
    macAuthStatus: Optional[bool] = False


class ClientControls(BaseModel):
    e0211bStatus: Optional[bool] = True
    e0211gStatus: Optional[bool] = True
    maxClientsPerBand: Optional[int] = 64


class FrameControls80211(BaseModel):
    advApName: Optional[bool] = False


class HighThroughputControl(BaseModel):
    enableAMpdu: Optional[bool] = True
    enableAMsdu: Optional[bool] = True


class Hotspot2(BaseModel):
    hotspot2Status: Optional[bool] = False


class RateControls(BaseModel):
    minRate24G: Optional[int] = 1
    minRate24GStatus: Optional[bool] = False
    minRate5G: Optional[int] = 6
    minRate5GStatus: Optional[bool] = False
    minRate6G: Optional[int] = 6
    minRate6GStatus: Optional[bool] = False


class PowerSaveControls(BaseModel):
    dtimInterval: Optional[int] = 1


class OptimizationSettings(BaseModel):
    broadcastFilterARP: Optional[bool] = False
    broadcastFilterAll: Optional[bool] = False
    broadcastKeyRotation: Optional[bool] = False
    broadcastKeyRotationTimeInterval: Optional[int] = 15
    clientsNumber: Optional[int] = 6
    e0211rStatus: Optional[bool] = False
    multicastChannelUtilization: Optional[int] = 90
    multicastOptimization: Optional[bool] = True
    okcStatus: Optional[bool] = False


class TrafficMapping(BaseModel):
    downlinks: Optional[List[int]] = []
    uplink: Optional[int] = 0


class Dot1pMapping(BaseModel):
    background: Optional[TrafficMapping] = TrafficMapping()
    bestEffort: Optional[TrafficMapping] = TrafficMapping()
    video: Optional[TrafficMapping] = TrafficMapping()
    voice: Optional[TrafficMapping] = TrafficMapping()


class DscpMapping(Dot1pMapping):
    trustOriginalDSCP: Optional[bool] = False


class QoSSetting(BaseModel):
    bandwidthContract: Optional[Dict[str, Any]] = {}
    broadcastMulticastOptimization: Optional[OptimizationSettings] = OptimizationSettings()
    dot1pMapping: Optional[Dot1pMapping] = Dot1pMapping()
    dot1pMappingEnable: Optional[bool] = True
    dscpMapping: Optional[DscpMapping] = DscpMapping()
    dscpMappingEnable: Optional[bool] = True


class RoamingControls(BaseModel):
    e0211kStatus: Optional[bool] = False
    e0211vStatus: Optional[bool] = False
    fdbUpdateStatus: Optional[bool] = False
    l3Roaming: Optional[bool] = False


class Security(BaseModel):
    classificationStatus: Optional[bool] = False
    clientIsolation: Optional[bool] = False
    macAuthPassProfileName: Optional[str] = "NONE"


class SSID(BaseModel):
    accessRoleProfile: Optional[AccessRoleProfile] = AccessRoleProfile()
    allowBand: Optional[str] = "All"
    mlo: Optional[bool] = False
    mloBand: Optional[str] = "All"
    authenticationStrategy: Optional[AuthenticationStrategy] = AuthenticationStrategy()
    byodRegistration: Optional[bool] = False
    clientControls: Optional[ClientControls] = ClientControls()
    deviceSpecificPSK: Optional[str] = "PREFER_DEVICE_SPECIFIC_PSK"
    dynamicPrivateGroupPSK: Optional[bool] = False
    dynamicVLAN: Optional[bool] = False
    enableSSID: Optional[bool] = True
    enhancedOpen: Optional[str] = "enable"
    essid: Optional[str] = ""
    frameControls802_11: Optional[FrameControls80211] = FrameControls80211()
    guestPortal: Optional[bool] = False
    hideSSID: Optional[bool] = False
    highThroughputControl: Optional[HighThroughputControl] = HighThroughputControl()
    hotspot2: Optional[Hotspot2] = Hotspot2()
    id: Optional[int] = 0
    minClientDataRateControls: Optional[RateControls] = RateControls()
    minMgmtRateControls: Optional[RateControls] = RateControls()
    name: Optional[str] = ""
    portalType: Optional[str] = "NO"
    powerSaveControls: Optional[PowerSaveControls] = PowerSaveControls()
    privateGroupPSK: Optional[bool] = False
    qosSetting: Optional[QoSSetting] = QoSSetting()
    replaceGroup: Optional[bool] = False
    roamingControls: Optional[RoamingControls] = RoamingControls()
    security: Optional[Security] = Security()
    securityLevel: Optional[str] = "Open"
    securityLevelUI: Optional[str] = "guestNetworkCase"
    uapsd: Optional[bool] = True
    useExistingAccessPolicy: Optional[bool] = False
    useExistingArp: Optional[bool] = True
    wepKeyIndex: Optional[int] = 0


class VlanTunnelMapping(BaseModel):
    mappingType: Optional[str] = "Vlan"
    useExistingTunnel: Optional[bool] = False
    vlans: Optional[List[str]] = []


class ScheduleConfig(BaseModel):
    alwaysAvailable: Optional[bool] = True


class Site(BaseModel):
    id: Optional[str] = ""
    name: Optional[str] = ""


class Group(BaseModel):
    id: Optional[str] = ""
    name: Optional[str] = ""


class Assignment(BaseModel):
    assignmentType: Optional[str] = "ASSIGN"
    configType: Optional[str] = "SSID"
    id: Optional[int] = 0
    mode: Optional[str] = "DEVICE_GROUP"
    vlanTunnelMapping: Optional[VlanTunnelMapping] = VlanTunnelMapping()
    scheduleConfig: Optional[ScheduleConfig] = ScheduleConfig()
    site: Optional[Site] = Site()
    group: Optional[Group] = Group()


class SSIDData(BaseModel):
    ssid: Optional[SSID] = SSID()
    assignments: Optional[List[Assignment]] = []

class Error(BaseModel):
    type: Optional[str] = None
    field: Optional[str] = None
    errorMsg: Optional[str] = None 

class SSIDResponse(BaseModel, Generic[T]):  # Inherit directly from BaseModel
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SSIDData] = None
    errorCode: Optional[int] = None
    errorMsg: Optional[str] = None
    errorDetailsCode: Optional[str] = None
    errorDetails: Optional[Union[str, dict]] = None  # Accept both str and dict
    errors: Optional[List[Error]] = None