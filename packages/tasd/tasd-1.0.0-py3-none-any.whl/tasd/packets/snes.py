from tasd.packet import _TASDPacketFactory as _TASD_PF, _VariableType as _VType, _VariableDefinition as _VDef, _EnumDefinition as _EDef
from tasd.constants import PacketType

'''
 4.3.3.1. SNES_LATCH_FILTER Packet
'''

SNESLatchFilter = _TASD_PF(
    "SNESLatchFilter",
    PacketType.SNES_LATCH_FILTER,
    [
        _VDef("time", _VType.UINT_16, 0)
    ]
)

'''
 4.3.3.2. SNES_CLOCK_FILTER Packet
'''

SNESClockFilter = _TASD_PF(
    "SNESClockFilter",
    PacketType.SNES_CLOCK_FILTER,
    [
        _VDef("time", _VType.UINT_8, 0)
    ]
)

'''
 4.3.3.3. SNES_GAME_GENIE_CODE Packet
'''

SNESGameGenieCode = _TASD_PF(
    "SNESGameGenieCode",
    PacketType.SNES_GAME_GENIE_CODE,
    [
        _VDef("code", _VType.STRING_EOP, "")
    ]
)

'''
 4.3.3.4. SNES_LATCH_TRAIN Packet
'''

SNESLatchTrain = _TASD_PF(
    "SNESLatchTrain",
    PacketType.SNES_LATCH_TRAIN,
    [
        _VDef("trains", _VType.LIST_UINT_64, None)
    ]
)