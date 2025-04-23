from tasd.packet import _TASDPacketFactory as _TASD_PF, _VariableType as _VType, _VariableDefinition as _VDef, _EnumDefinition as _EDef
from tasd.constants import PacketType

'''
 4.3.5.1. INPUT_CHUNK Packet 
'''

InputChunk = _TASD_PF(
    "InputChunk",
    PacketType.INPUT_CHUNK,
    [
        _VDef("port", _VType.UINT_8, 1),
        _VDef("data", _VType.BYTES_EOP, b"")
    ]
)

'''
 4.3.5.2. INPUT_MOMENT Packet
'''

class INPUT_MOMENT_INDEX_TYPE():
    FRAME              = 0x01
    CYCLE_COUNT        = 0x02
    MILLISECONDS       = 0x03
    MICROSECONDS_X10   = 0x04
InputMoment = _TASD_PF(
    "InputMoment",
    PacketType.INPUT_MOMENT,
    [
        _VDef("port", _VType.UINT_8, 1),
        _VDef("hold", _VType.BOOL, False),
        _VDef("index_type", _VType.UINT_8, INPUT_MOMENT_INDEX_TYPE.FRAME),
        _VDef("index", _VType.UINT_64, 0),
        _VDef("inputs", _VType.BYTES_EOP, b"")
    ],
    [
        _EDef("INPUT_MOMENT_INDEX_TYPE", INPUT_MOMENT_INDEX_TYPE)
    ]
)

'''
 4.3.5.3. TRANSITION Packet
'''

class TRANSITION_INDEX_TYPE():
    FRAME               = 0x01
    CYCLE_COUNT         = 0x02
    MILLISECONDS        = 0x03
    MICROSECONDS        = 0x04
    NANOSECONDS         = 0x05
    INPUT_CHUNK_INDEX   = 0x06
class TRANSITION_TYPE():
    SOFT_RESET          = 0x01
    POWER_RESET         = 0x02
    RESTART_TASD_FILE   = 0x03
    PACKET_DERIVED      = 0xFF
Transition = _TASD_PF(
    "Transition",
    PacketType.TRANSITION,
    [
        _VDef("port", _VType.UINT_8, 1),
        _VDef("index_type", _VType.UINT_8, TRANSITION_INDEX_TYPE.FRAME),
        _VDef("index", _VType.UINT_64, 0),
        _VDef("type", _VType.UINT_8, TRANSITION_TYPE.SOFT_RESET),
        _VDef("packet", _VType.BYTES_EOP, b"")
    ],
    [
        _EDef("TRANSITION_INDEX_TYPE", TRANSITION_INDEX_TYPE),
        _EDef("TRANSITION_TYPE", TRANSITION_TYPE)
    ]
)

'''
 4.3.5.4. LAG_FRAME_CHUNK Packet
'''

LagFrameChunk = _TASD_PF(
    "LagFrameChunk",
    PacketType.LAG_FRAME_CHUNK,
    [
        _VDef("frame", _VType.UINT_32, 0),
        _VDef("count", _VType.UINT_32, 0)
    ]
)

'''
 4.3.5.5. MOVIE_TRANSITION
'''

class MOVIE_TRANSITION_TYPE():
    SOFT_RESET          = 0x01
    POWER_RESET         = 0x02
    RESTART_TASD_FILE   = 0x03
    PACKET_DERIVED      = 0xFF
MovieTransition = _TASD_PF(
    "MovieTransition",
    PacketType.MOVIE_TRANSITION,
    [
        _VDef("frame", _VType.UINT_32, 0),
        _VDef("type", _VType.UINT_8, MOVIE_TRANSITION_TYPE.SOFT_RESET),
        _VDef("packet", _VType.BYTES_EOP, b"")
    ],
    [
        _EDef("MOVIE_TRANSITION_TYPE", MOVIE_TRANSITION_TYPE),
    ]
)