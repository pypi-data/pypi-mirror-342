class _MetaPacketType():
    def __init_subclass__(self):
        keys = [key for key in self.__dict__.keys() if type(self.__dict__[key]) == int]
        self._key2name = dict()
        for key in keys:
            self._key2name[self.__dict__[key]] = key

class PacketType(_MetaPacketType):
    # General Keys
    CONSOLE_TYPE                = 0x0001
    CONSOLE_REGION              = 0x0002
    GAME_TITLE                  = 0x0003
    ROM_NAME                    = 0x0004
    ATTRIBUTION                 = 0x0005
    CATEGORY                    = 0x0006
    EMULATOR_NAME               = 0x0007
    EMULATOR_VERSION            = 0x0008
    EMULATOR_CORE               = 0x0009
    TAS_LAST_MODIFIED           = 0x000A
    DUMP_CREATED                = 0x000B
    DUMP_LAST_MODIFIED          = 0x000C
    TOTAL_FRAMES                = 0x000D
    RERECORDS                   = 0x000E
    SOURCE_LINK                 = 0x000F
    BLANK_FRAMES                = 0x0010
    VERIFIED                    = 0x0011
    MEMORY_INIT                 = 0x0012
    GAME_IDENTIFIER             = 0x0013
    MOVIE_LICENSE               = 0x0014
    MOVIE_FILE                  = 0x0015
    PORT_CONTROLLER             = 0x00F0
    PORT_OVERREAD               = 0x00F1
    # NES Specific Keys
    NES_LATCH_FILTER            = 0x0101
    NES_CLOCK_FILTER            = 0x0102
    NES_GAME_GENIE_CODE         = 0x0104
    # SNES Specific Keys
    SNES_LATCH_FILTER           = 0x0201
    SNES_CLOCK_FILTER           = 0x0202
    SNES_GAME_GENIE_CODE        = 0x0204
    SNES_LATCH_TRAIN            = 0x0205
    # Genesis Specific Keys
    GENESIS_GAME_GENIE_CODE     = 0x0804
    # Input Frame/Timing Keys
    INPUT_CHUNK                 = 0xFE01
    INPUT_MOMENT                = 0xFE02
    TRANSITION                  = 0xFE03
    LAG_FRAME_CHUNK             = 0xFE04
    MOVIE_TRANSITION            = 0xFE05
    # Extraneous Keys
    COMMENT                     = 0xFF01
    EXPERIMENTAL                = 0xFFFE
    UNSPECIFIED                 = 0xFFFF
    @classmethod
    def lookup(cls, key):
        return cls._key2name.get(key, f'UNKNOWN_PACKET_{key:04X}')
