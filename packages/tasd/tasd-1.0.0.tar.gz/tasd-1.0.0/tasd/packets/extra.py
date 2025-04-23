from tasd.packet import _TASDPacketFactory as _TASD_PF, _VariableType as _VType, _VariableDefinition as _VDef, _EnumDefinition as _EDef
from tasd.constants import PacketType

'''
 4.3.6.1. COMMENT Packet
'''

Comment = _TASD_PF(
    "Comment",
    PacketType.COMMENT,
    [
        _VDef("comment", _VType.STRING_EOP, "")
    ]
)

'''
 4.3.6.2. EXPERIMENTAL Packet
'''

Experimental = _TASD_PF(
    "Experimental",
    PacketType.EXPERIMENTAL,
    [
        _VDef("experimental", _VType.BOOL, False)
    ]
)

'''
 4.3.6.3. UNSPECIFIED Packet
'''

Unspecified = _TASD_PF(
    "Unspecified",
    PacketType.UNSPECIFIED,
    [
        _VDef("data", _VType.BYTES_EOP, b"")
    ]
)