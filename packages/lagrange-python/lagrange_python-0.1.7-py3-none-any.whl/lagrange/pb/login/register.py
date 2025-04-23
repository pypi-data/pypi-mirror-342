import random

from lagrange.info import AppInfo, DeviceInfo
from lagrange.pb.message.msg_push import MsgPushBody
from lagrange.utils.binary.protobuf import proto_field, ProtoStruct


# trpc.qq_new_tech.status_svc.StatusService.Register
class _DeviceInfo(ProtoStruct):
    device_name: str = proto_field(1)
    vendor_os: str = proto_field(2)
    system_kernel: str = proto_field(3)
    vendor_name: str = proto_field(4, default="")
    vendor_os_lower: str = proto_field(5)


class PBRegisterRequest(ProtoStruct):
    guid: str = proto_field(1)
    kick_pc: int = proto_field(2, default=0)  # ?
    current_version: str = proto_field(3)
    field_4: int = proto_field(4, default=0)  # IsFirstRegisterProxyOnline
    locale_id: int = proto_field(5, default=2052)
    device_info: _DeviceInfo = proto_field(6)
    set_mute: int = proto_field(7, default=0)  # ?
    register_vendor_type: int = proto_field(8, default=0)  # ?
    register_type: int = proto_field(9, default=1)

    @classmethod
    def build(cls, app: AppInfo, device: DeviceInfo) -> "PBRegisterRequest":
        return cls(
            guid=device.guid.upper(),
            current_version=app.current_version,
            device_info=_DeviceInfo(
                device_name=device.device_name,
                vendor_os=app.vendor_os.capitalize(),
                system_kernel=device.system_kernel,
                vendor_os_lower=app.vendor_os,
            ),
        )


class PBRegisterResponse(ProtoStruct):
    message: str = proto_field(2)
    timestamp: int = proto_field(3)


# trpc.msg.register_proxy.RegisterProxy.SsoInfoSync
class C2cMsgCookie(ProtoStruct):
    last_msg_time: int = proto_field(1)


class SsoC2cInfo(ProtoStruct):
    msg_cookie: C2cMsgCookie = proto_field(1)
    last_msg_time: int = proto_field(2)
    last_msg_cookie: C2cMsgCookie = proto_field(3)

    @classmethod
    def build(cls, last_msg_time=0) -> "SsoC2cInfo":
        return cls(
            msg_cookie=C2cMsgCookie(last_msg_time=last_msg_time),
            last_msg_cookie=C2cMsgCookie(last_msg_time=last_msg_time),
            last_msg_time=last_msg_time,
        )


class NormalCfg(ProtoStruct):
    int_cfg: dict = proto_field(1, default=None)  # dict[int, int]


class CurrentAppState(ProtoStruct):
    is_delay_request: bool = proto_field(1)
    app_state: int = proto_field(2)
    silence_state: int = proto_field(3)

    @classmethod
    def build(cls) -> "CurrentAppState":
        return cls(
            is_delay_request=False,
            app_state=0,
            silence_state=0,
        )


class UnknownInfo(ProtoStruct):
    grp_code: int = proto_field(1, default=0)
    f2: int = proto_field(2, default=2)


class PBSsoInfoSyncRequest(ProtoStruct):
    sync_flag: int = proto_field(1)
    req_rand: int = proto_field(2)
    current_active_stats: int = proto_field(4)
    grp_last_msg_time: int = proto_field(5)
    c2c_info: SsoC2cInfo = proto_field(6)
    normal_cfg: NormalCfg = proto_field(8)
    register_info: PBRegisterRequest = proto_field(9)
    unknown_f10: UnknownInfo = proto_field(10)
    app_state: CurrentAppState = proto_field(11)

    @classmethod
    def build(cls, app: AppInfo, device: DeviceInfo) -> "PBSsoInfoSyncRequest":
        return cls(
            sync_flag=735,
            req_rand=random.randint(114, 514),  # ?
            current_active_stats=2,
            grp_last_msg_time=0,
            c2c_info=SsoC2cInfo.build(),
            normal_cfg=NormalCfg(int_cfg=dict()),
            register_info=PBRegisterRequest.build(app, device),
            unknown_f10=UnknownInfo(),
            app_state=CurrentAppState.build()
        )


class PBSsoInfoSyncResponse(ProtoStruct):
    # f3: int = proto_field(3)
    # f4: int = proto_field(4)
    # f6: int = proto_field(6)
    reg_rsp: PBRegisterResponse = proto_field(7)
    # f9: int = proto_field(9)


# trpc.msg.register_proxy.RegisterProxy.InfoSyncPush: From Server
class InfoSyncPushGrpInfo(ProtoStruct):
    grp_id: int = proto_field(1)
    last_msg_seq: int = proto_field(2)
    last_msg_seq_read: int = proto_field(3)  # bot最后一次标记已读
    f4: int = proto_field(4)  # 1
    last_msg_timestamp: int = proto_field(8, default=0)
    grp_name: str = proto_field(9)
    last_msg_seq_sent: int = proto_field(10, default=0)  # bot最后一次发信 TODO: 可能不太对？确认下
    f10: int = proto_field(10, default=None)  # u32, unknown
    f12: int = proto_field(12, default=None)  # 1
    f13: int = proto_field(13, default=None)  # 1
    f14: int = proto_field(14, default=None)  # u16?
    f15: int = proto_field(15, default=None)  # 1
    f16: int = proto_field(16, default=None)  # u16?


class InnerGrpMsg(ProtoStruct):
    grp_id: int = proto_field(3)
    start_seq: int = proto_field(4)
    end_seq: int = proto_field(5)
    msgs: list[MsgPushBody] = proto_field(6)  # last 30 msgs
    last_msg_time: int = proto_field(8)


class InfoSyncGrpMsgs(ProtoStruct):
    inner: list[InnerGrpMsg] = proto_field(3)


class InnerSysEvt(ProtoStruct):
    grp_id: int = proto_field(1)
    grp_id_str: str = proto_field(2)
    last_evt_time: int = proto_field(5)
    events: list[MsgPushBody] = proto_field(8)  # TODO: parse event (like MsgPush?)


# with FriendMessage
class InfoSyncSysEvents(ProtoStruct):
    # f3: dict = proto_field(3)  # {1: LAST_EVT_TIME}
    inner: list[InnerSysEvt] = proto_field(4)
    # f5: dict = proto_field(5)  # {1: LAST_EVT_TIME}


class PBSsoInfoSyncPush(ProtoStruct):
    cmd_type: int = proto_field(3)  # 5: GrpInfo(f6), 2: HUGE msg push block(f7&f8), 1&4: unknown(empty)
    f4: int = proto_field(4)  # 393
    grp_info: list[InfoSyncPushGrpInfo] = proto_field(6, default=None)
    grp_msgs: InfoSyncGrpMsgs = proto_field(7, default=None)
    sys_events: InfoSyncSysEvents = proto_field(8, default=None)


# trpc.msg.register_proxy.RegisterProxy.PushParams
class PPOnlineDevices(ProtoStruct):
    sub_id: int = proto_field(1)
    # f2: int = proto_field(2)  # 2
    # f3: int = proto_field(3)  # 1
    # f4: int = proto_field(4)  # 109
    os_name: str = proto_field(5)
    # f6:int = proto_field(6)
    device_name: str = proto_field(7)


class PBServerPushParams(ProtoStruct):
    online_devices: list[PPOnlineDevices] = proto_field(4, default_factory=list)
    # f6: dict = proto_field(6)  # {2: 9}
    # f7: str = proto_field(7)  # value: ""(empty)
    # f8: list[int] = proto_field(8)  # multi long int
    # f9: int = proto_field(9)  # 8640000, 100days
