from tasd.packet import _TASDPacketFactory as _TASD_PF, _VariableType as _VType, _VariableDefinition as _VDef, _EnumDefinition as _EDef
from tasd.constants import PacketType

'''
 4.3.2.1. NES_LATCH_FILTER Packet
'''

NESLatchFilter = _TASD_PF(
    "NESLatchFilter",
    PacketType.NES_LATCH_FILTER,
    [
        _VDef("time", _VType.UINT_16, 0)
    ]
)

'''
 4.3.2.2. NES_CLOCK_FILTER Packet
'''

NESClockFilter = _TASD_PF(
    "NESClockFilter",
    PacketType.NES_CLOCK_FILTER,
    [
        _VDef("time", _VType.UINT_8, 0)
    ]
)

'''
 4.3.2.3. NES_GAME_GENIE_CODE Packet
'''

NESGameGenieCode = _TASD_PF(
    "NESGameGenieCode",
    PacketType.NES_GAME_GENIE_CODE,
    [
        _VDef("code", _VType.STRING_EOP, "")
    ]
)