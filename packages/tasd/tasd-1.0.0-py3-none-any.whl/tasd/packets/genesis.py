from tasd.packet import _TASDPacketFactory as _TASD_PF, _VariableType as _VType, _VariableDefinition as _VDef, _EnumDefinition as _EDef
from tasd.constants import PacketType

'''
 4.3.4.1. GENESIS_GAME_GENIE_CODE Packet
'''

GenesisGameGenieCode = _TASD_PF(
    "GenesisGameGenieCode",
    PacketType.GENESIS_GAME_GENIE_CODE,
    [
        _VDef("code", _VType.STRING_EOP, "")
    ]
)

__all__ = [
    GenesisGameGenieCode
]