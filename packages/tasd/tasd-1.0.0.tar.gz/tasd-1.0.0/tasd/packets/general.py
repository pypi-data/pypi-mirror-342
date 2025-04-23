from tasd.packet import _TASDPacketFactory as _TASD_PF, _VariableType as _VType, _VariableDefinition as _VDef, _EnumDefinition as _EDef
from tasd.constants import PacketType

'''
 4.3.1.1. CONSOLE_TYPE Packet
'''

class CONSOLE_TYPE():
    NES       = 0x01
    SNES      = 0x02
    N64       = 0x03
    GC        = 0x04
    GB        = 0x05
    GBC       = 0x06
    GBA       = 0x07
    GENESIS   = 0x08
    A2600     = 0x09
    CUSTOM    = 0xFF
ConsoleType = _TASD_PF(
    "ConsoleType",
    PacketType.CONSOLE_TYPE,
    [
        _VDef("console", _VType.UINT_8, CONSOLE_TYPE.NES),
        _VDef("name", _VType.STRING_EOP, "")
    ],
    [
        _EDef("CONSOLE_TYPE", CONSOLE_TYPE)
    ]
)

'''
 4.3.1.2. CONSOLE_REGION Packet
'''

class CONSOLE_REGION():
    NTSC    = 0x01
    PAL     = 0x02
    OTHER   = 0xFF
ConsoleRegion = _TASD_PF(
    "ConsoleRegion",
    PacketType.CONSOLE_REGION,
    [
        _VDef("region", _VType.UINT_8, CONSOLE_REGION.NTSC)
    ],
    [
        _EDef("CONSOLE_REGION", CONSOLE_REGION)
    ]
)

'''
 4.3.1.3. GAME_TITLE Packet
'''

GameTitle = _TASD_PF(
    "GameTitle",
    PacketType.GAME_TITLE,
    [
        _VDef("title", _VType.STRING_EOP, "")
    ]
)


'''
 4.3.1.4. ROM_NAME Packet
'''

RomName = _TASD_PF(
    "RomName",
    PacketType.ROM_NAME,
    [
        _VDef("name", _VType.STRING_EOP, "")
    ]
)

'''
 4.3.1.5. ATTRIBUTION Packet
'''

class ATTRIBUTION_TYPE():
    AUTHOR              = 0x01
    VERIFIER            = 0x02
    TASD_FILE_CREATOR   = 0x03
    TASD_FILE_EDITOR    = 0x04
    OTHER               = 0xFF
Attribution = _TASD_PF(
    "Attribution",
    PacketType.ATTRIBUTION,
    [
        _VDef("type", _VType.UINT_8, ATTRIBUTION_TYPE.AUTHOR),
        _VDef("name", _VType.STRING_EOP, "")
    ],
    [
        _EDef("ATTRIBUTION_TYPE", ATTRIBUTION_TYPE)
    ]
)


'''
 4.3.1.6. CATEGORY Packet
'''

Category = _TASD_PF(
    "Category",
    PacketType.CATEGORY,
    [
        _VDef("category", _VType.STRING_EOP, "")
    ]
)

'''
 4.3.1.7. EMULATOR_NAME Packet
'''

EmulatorName = _TASD_PF(
    "EmulatorName",
    PacketType.EMULATOR_NAME,
    [
        _VDef("name", _VType.STRING_EOP, "")
    ]
)

'''
 4.3.1.8. EMULATOR_VERSION Packet
'''

EmulatorVersion = _TASD_PF(
    "EmulatorVersion",
    PacketType.EMULATOR_VERSION,
    [
        _VDef("version", _VType.STRING_EOP, "")
    ]
)

'''
 4.3.1.9. EMULATOR_CORE Packet
'''

EmulatorCore = _TASD_PF(
    "EmulatorCore",
    PacketType.EMULATOR_CORE,
    [
        _VDef("core", _VType.STRING_EOP, "")
    ]
)

'''
 4.3.1.10. TAS_LAST_MODIFIED Packet
'''

TASLastModified = _TASD_PF(
    "TASLastModified",
    PacketType.TAS_LAST_MODIFIED,
    [
        _VDef("timestamp", _VType.INT_64, 0)
    ]
)

'''
 4.3.1.11. DUMP_CREATED Packet
'''

DumpCreated = _TASD_PF(
    "DumpCreated",
    PacketType.DUMP_CREATED,
    [
        _VDef("timestamp", _VType.INT_64, 0)
    ]
)

'''
 4.3.1.12. DUMP_LAST_MODIFIED Packet
'''

DumpLastModified = _TASD_PF(
    "DumpLastModified",
    PacketType.DUMP_LAST_MODIFIED,
    [
        _VDef("timestamp", _VType.INT_64, 0)
    ]
)

'''
 4.3.1.13. TOTAL_FRAMES Packet
'''

TotalFrames = _TASD_PF(
    "TotalFrames",
    PacketType.TOTAL_FRAMES,
    [
        _VDef("frames", _VType.UINT_32, 0)
    ]
)

'''
 4.3.1.14. RERECORDS Packet
'''

Rerecords = _TASD_PF(
    "Rerecords",
    PacketType.RERECORDS,
    [
        _VDef("rerecords", _VType.UINT_32, 0)
    ]
)

'''
 4.3.1.15. SOURCE_LINK Packet
'''

SourceLink = _TASD_PF(
    "SourceLink",
    PacketType.SOURCE_LINK,
    [
        _VDef("link", _VType.STRING_EOP, "")
    ]
)

'''
 4.3.1.16. BLANK_FRAMES Packet
'''

BlankFrames = _TASD_PF(
    "BlankFrames",
    PacketType.BLANK_FRAMES,
    [
        _VDef("frames", _VType.INT_16, 0)
    ]
)

'''
 4.3.1.17. VERIFIED Packet
'''

Verified = _TASD_PF(
    "Verified",
    PacketType.VERIFIED,
    [
        _VDef("verified", _VType.BOOL, False)
    ]
)

'''
 4.3.1.18. MEMORY_INIT Packet
'''

class MEMORY_INIT_TYPE():
    NONE                       = 0x01
    ALL_00                     = 0x02
    ALL_FF                     = 0x03
    PATTERN_00000000FFFFFFFF   = 0x04
    RANDOM                     = 0x05
    CUSTOM                     = 0xFF
class MEMORY_INIT_DEVICE():
    NES_CPU_RAM         = 0x0101
    NES_CART_SRAM       = 0x0102
    SNES_CPU_RAM        = 0x0201
    SNES_CART_SRAM      = 0x0202
    GB_CPU_RAM          = 0x0501
    GB_CART_SRAM        = 0x0502
    GBC_CPU_RAM         = 0x0601
    GBC_CART_SRAM       = 0x0602
    GBA_CPU_RAM         = 0x0701
    GBA_CART_SRAM       = 0x0702
    GENESIS_CPU_RAM     = 0x0801
    GENESIS_CART_SRAM   = 0x0802
    A2600_CPU_RAM       = 0x0901
    A2600_CART_SRAM     = 0x0902
    CUSTOM              = 0xFFFF
MemoryInit = _TASD_PF(
    "MemoryInit",
    PacketType.MEMORY_INIT,
    [
        _VDef("type", _VType.UINT_8, MEMORY_INIT_TYPE.NONE),
        _VDef("device", _VType.UINT_16, MEMORY_INIT_DEVICE.NES_CPU_RAM),
        _VDef("required", _VType.BOOL, False),
        _VDef("name", _VType.STRING_PLEN, ""),
        _VDef("data", _VType.BYTES_EOP, b"")
    ],
    [
        _EDef("MEMORY_INIT_TYPE", MEMORY_INIT_TYPE),
        _EDef("MEMORY_INIT_DEVICE", MEMORY_INIT_DEVICE)
    ]
)

'''
 4.3.1.19. GAME_IDENTIFIER Packet
'''

class GAME_IDENTIFIER_TYPE():
    MD5          = 0x01
    SHA1         = 0x02
    SHA224       = 0x03
    SHA256       = 0x04
    SHA384       = 0x05
    SHA512       = 0x06
    SHA512_224   = 0x07
    SHA512_256   = 0x08
    SHA3_224     = 0x09
    SHA3_256     = 0x0A
    SHA3_384     = 0x0B
    SHA3_512     = 0x0C
    SHAKE_128    = 0x0D
    SHAKE_256    = 0x0E
    OTHER        = 0xFF
class GAME_IDENTIFIER_BASE():
    RAW_BINARY   = 0x01
    BASE16       = 0x02
    BASE32       = 0x03
    BASE64       = 0x04
    OTHER        = 0xFF
GameIdentifier = _TASD_PF(
    "GameIdentifier",
    PacketType.GAME_IDENTIFIER,
    [
        _VDef("type", _VType.UINT_8, GAME_IDENTIFIER_TYPE.MD5),
        _VDef("encoding", _VType.UINT_8, GAME_IDENTIFIER_BASE.RAW_BINARY),
        _VDef("name", _VType.STRING_PLEN, ""),
        _VDef("identifier", _VType.BYTES_EOP, b"")
    ],
    [
        _EDef("GAME_IDENTIFIER_TYPE", GAME_IDENTIFIER_TYPE),
        _EDef("GAME_IDENTIFIER_BASE", GAME_IDENTIFIER_BASE)
    ])

'''
 4.3.1.20. MOVIE_LICENSE Packet
'''

MovieLicense = _TASD_PF(
    "MovieLicense",
    PacketType.MOVIE_LICENSE,
    [
        _VDef("link", _VType.STRING_EOP, "")
    ]
)

'''
 4.3.1.21. MOVIE_FILE Packet
'''

MovieFile = _TASD_PF(
    "MovieFile",
    PacketType.MOVIE_FILE,
    [
        _VDef("name", _VType.STRING_PLEN, ""),
        _VDef("data", _VType.BYTES_EOP, b"")
    ]
)

'''
 4.3.1.22. PORT_CONTROLLER Packet
'''

class CONTROLLER_TYPE():
    NES_STANDARD_CONTROLLER                       = 0x0101
    NES_FOUR_SCORE                                = 0x0102
    NES_ZAPPER                                    = 0x0103
    NES_POWER_PAD                                 = 0x0104
    FAMICOM_FAMILY_BASIC_KEYBOARD                 = 0x0105
    SNES_STANDARD_CONTROLLER                      = 0x0201
    SNES_SUPER_MULTITAP                           = 0x0202
    SNES_MOUSE                                    = 0x0203
    SNES_SUPERSCOPE                               = 0x0204
    N64_STANDARD_CONTROLLER                       = 0x0301
    N64_STANDARD_CONTROLLER_WITH_RUMBLE_PAK       = 0x0302
    N64_STANDARD_CONTROLLER_WITH_CONTROLLER_PAK   = 0x0303
    N64_STANDARD_CONTROLLER_WITH_TRANSFER_PAK     = 0x0304
    N64_MOUSE                                     = 0x0305
    N64_VOICE_RECOGNITION_UNIT                    = 0x0306
    N64_RANDNET_KEYBOARD                          = 0x0307
    N64_DENSHA_DE_GO                              = 0x0308
    GC_STANDARD_CONTROLLER                        = 0x0401
    GC_KEYBOARD                                   = 0x0402
    GB_GAMEPAD                                    = 0x0501
    GBC_GAMEPAD                                   = 0x0601
    GBA_GAMEPAD                                   = 0x0701
    GENESIS_3BUTTON                               = 0x0801
    GENESIS_6BUTTON                               = 0x0802
    A2600_JOYSTICK                                = 0x0901
    A2600_PADDLE                                  = 0x0902
    A2600_KEYBOARD_CONTROLLER                     = 0x0903
    OTHER_UNSPECIFIED                             = 0xFFFF
PortController = _TASD_PF(
    "PortController",
    PacketType.PORT_CONTROLLER,
    [
        _VDef("port", _VType.UINT_8, 1),
        _VDef("type", _VType.UINT_16, CONTROLLER_TYPE.NES_STANDARD_CONTROLLER)
    ],
    [
        _EDef("CONTROLLER_TYPE", CONTROLLER_TYPE)
    ]
)

'''
 4.3.1.23. PORT_OVERREAD Packet
'''

PortOverread = _TASD_PF(
    "PortOverread",
    PacketType.PORT_OVERREAD,
    [
        _VDef("port", _VType.UINT_8, 1),
        _VDef("high", _VType.BOOL, False)
    ]
)
