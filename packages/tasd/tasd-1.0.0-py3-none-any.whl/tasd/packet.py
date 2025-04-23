from typing import NamedTuple, List, Any
from enum import Enum

from tasd.constants import PacketType
from tasd.utils import *

class _VariableType(Enum):
    STRING_EOP     = 0x00
    STRING_PLEN    = 0x01
    STRING_PEXP    = 0x02
    BYTES_EOP      = 0x10
    BYTES_PLEN     = 0x11
    BYTES_PEXP     = 0x12
    INT_8          = 0x20
    INT_16         = 0x21
    INT_24         = 0x22
    INT_32         = 0x23
    INT_64         = 0x24
    INT_N          = 0x25
    UINT_8         = 0x30
    UINT_16        = 0x31
    UINT_24        = 0x32
    UINT_32        = 0x33
    UINT_64        = 0x34
    UINT_N         = 0x35
    BOOL           = 0x40
    LIST_UINT_64   = 0x50


class _VariableDefinition(NamedTuple):
    name: str
    type: _VariableType
    default: Any

class _EnumDefinition(NamedTuple):
    name: str
    enum: Enum

class _TASDPacket():
    @classmethod
    def from_bytes(cls, buffer: bytes):
        self = cls()
        index = 0
        for variable in cls._variables:
            match variable.type:
                case _VariableType.STRING_EOP:
                    setattr(self, variable.name, readString(buffer, index, len(buffer) - index))
                    index = len(buffer)
                case _VariableType.STRING_PLEN:
                    plen = readInt8(buffer, index)
                    index += 1
                    setattr(self, variable.name, readString(buffer, index, plen))
                    index += plen
                case _VariableType.STRING_PEXP:
                    pexp = readInt8(buffer, index)
                    index += 1
                    plen = readIntN(buffer, index, pexp)
                    index += pexp
                    setattr(self, variable.name, readString(buffer, index, plen))
                    index += plen
                case _VariableType.BYTES_EOP:
                    setattr(self, variable.name, readBytes(buffer, index, len(buffer)))
                    index = len(buffer)
                case _VariableType.BYTES_PLEN:
                    plen = readInt8(buffer, index)
                    index += 1
                    setattr(self, variable.name, readBytes(buffer, index, plen))
                    index += plen
                case _VariableType.BYTES_PEXP:
                    pexp = readInt8(buffer, index)
                    index += 1
                    plen = readIntN(buffer, index, pexp)
                    index += pexp
                    setattr(self, variable.name, readBytes(buffer, index, plen))
                    index += plen
                case _VariableType.INT_8:
                    setattr(self, variable.name, readInt8(buffer, index))
                    index += 1
                case _VariableType.INT_16:
                    setattr(self, variable.name, readInt16(buffer, index))
                    index += 2
                case _VariableType.INT_24:
                    setattr(self, variable.name, readInt24(buffer, index))
                    index += 3
                case _VariableType.INT_32:
                    setattr(self, variable.name, readInt32(buffer, index))
                    index += 4
                case _VariableType.INT_64:
                    setattr(self, variable.name, readInt64(buffer, index))
                    index += 8
                case _VariableType.INT_N:
                    pexp = readInt8(buffer, index)
                    index += 1
                    setattr(self, variable.name, readIntN(buffer, index, pexp))
                    index += pexp
                case _VariableType.UINT_8:
                    setattr(self, variable.name, readUint8(buffer, index))
                    index += 1
                case _VariableType.UINT_16:
                    setattr(self, variable.name, readUint16(buffer, index))
                    index += 2
                case _VariableType.UINT_24:
                    setattr(self, variable.name, readUint24(buffer, index))
                    index += 3
                case _VariableType.UINT_32:
                    setattr(self, variable.name, readUint32(buffer, index))
                    index += 4
                case _VariableType.UINT_64:
                    setattr(self, variable.name, readUint64(buffer, index))
                    index += 8
                case _VariableType.UINT_N:
                    pexp = readUint8(buffer, index)
                    index += 1
                    setattr(self, variable.name, readUintN(buffer, index, pexp))
                    index += pexp
                case _VariableType.BOOL:
                    setattr(self, variable.name, readBoolean(buffer, index))
                    index += 1
                case _VariableType.LIST_UINT_64:
                    l = list()
                    while index < len(buffer):
                        l.append(readUint64(buffer, index))
                        index += 8
                    setattr(self, variable.name, l)
                case _:
                    raise ValueError("Unknown Variable Type", variable)
        return self
    def size(self):
        size = 0
        for variable in self._variables:
            value = getattr(self, variable.name)
            match variable.type:
                case _VariableType.STRING_EOP:
                    size += sizeString(value)
                case _VariableType.STRING_PLEN:
                    size += ( 1 + sizeString(value) )
                case _VariableType.STRING_PEXP:
                    vsize = sizeString(value)
                    size += ( 1 + minUint(vsize) + vsize )
                case _VariableType.BYTES_EOP:
                    size += len(value)
                case _VariableType.BYTES_PLEN:
                    size += ( 1 + len(value) )
                case _VariableType.BYTES_PEXP:
                    vsize = len(value)
                    size += ( 1 + minUint(vsize) + vsize )
                case _VariableType.INT_8:
                    size += 1
                case _VariableType.INT_16:
                    size += 2
                case _VariableType.INT_24:
                    size += 3
                case _VariableType.INT_32:
                    size += 4
                case _VariableType.INT_64:
                    size += 8
                case _VariableType.INT_N:
                    size += minInt(value)
                case _VariableType.UINT_8:
                    size += 1
                case _VariableType.UINT_16:
                    size += 2
                case _VariableType.UINT_24:
                    size += 3
                case _VariableType.UINT_32:
                    size += 4
                case _VariableType.UINT_64:
                    size += 8
                case _VariableType.UINT_N:
                    size += minUint(value)
                case _VariableType.BOOL:
                    size += 1
                case _VariableType.LIST_UINT_64:
                    size += ( 8 * len(value) )
                case _:
                    raise ValueError("Unknown Variable Type", variable)
        return size
    def to_bytes(self):
        buffer = bytearray(self.size())
        index = 0
        for variable in self._variables:
            value = getattr(self, variable.name)
            match variable.type:
                case _VariableType.STRING_EOP:
                    writeString(value, buffer, index)
                    index += sizeString(value)
                case _VariableType.STRING_PLEN:
                    plen = sizeString(value)
                    writeUint8(plen, buffer, index)
                    index += 1
                    writeString(value, buffer, index)
                    index += plen
                case _VariableType.STRING_PEXP:
                    plen = sizeString(value)
                    pexp = minUint(plen)
                    writeUint8(pexp, buffer, index)
                    index += 1
                    writeUintN(plen, buffer, index, pexp)
                    index += pexp
                    writeString(value, buffer, index)
                    index += plen
                case _VariableType.BYTES_EOP:
                    writeBytes(value, buffer, index)
                    index += len(value)
                case _VariableType.BYTES_PLEN:
                    plen = len(value)
                    writeUint8(plen, buffer, index)
                    index += 1
                    writeBytes(value, buffer, index)
                    index += plen
                case _VariableType.BYTES_PEXP:
                    plen = len(value)
                    pexp = minUint(plen)
                    writeUint8(pexp, buffer, index)
                    index += 1
                    writeUintN(plen, buffer, index, pexp)
                    index += pexp
                    writeBytes(value, buffer, index)
                    index += plen
                case _VariableType.INT_8:
                    writeInt8(value, buffer, index)
                    index += 1
                case _VariableType.INT_16:
                    writeInt16(value, buffer, index)
                    index += 2
                case _VariableType.INT_24:
                    writeInt24(value, buffer, index)
                    index += 3
                case _VariableType.INT_32:
                    writeInt32(value, buffer, index)
                    index += 4
                case _VariableType.INT_64:
                    writeInt64(value, buffer, index)
                    index += 8
                case _VariableType.INT_N:
                    pexp = minInt(value)
                    writeUint8(pexp, buffer, index)
                    index += 1
                    writeIntN(value, buffer, index, pexp)
                    index += pexp
                case _VariableType.UINT_8:
                    writeUint8(value, buffer, index)
                    index += 1
                case _VariableType.UINT_16:
                    writeUint16(value, buffer, index)
                    index += 2
                case _VariableType.UINT_24:
                    writeUint24(value, buffer, index)
                    index += 3
                case _VariableType.UINT_32:
                    writeUint32(value, buffer, index)
                    index += 4
                case _VariableType.UINT_64:
                    writeUint64(value, buffer, index)
                    index += 8
                case _VariableType.UINT_N:
                    pexp = minInt(value)
                    writeUint8(pexp, buffer, index)
                    index += 1
                    writeUintN(value, buffer, index, pexp)
                    index += pexp
                case _VariableType.BOOL:
                    writeBoolean(value, buffer, index)
                    index += 1
                case _VariableType.LIST_UINT_64:
                    for val in value:
                        writeUint64(val, buffer, index)
                        index += 8
                case _:
                    raise ValueError("Unknown Variable Type", variable)
        return buffer
    def __repr__(self):
        return f"{self._name}({', '.join(f'{var.name}={getattr(self, var.name)}' for var in self._variables)})"

_lookup_table = dict()

def _TASDPacketFactory(name: str, key: int, variables: List[_VariableDefinition] = [], enums: List[_EnumDefinition] = []):
    class Packet(_TASDPacket):
        _variables = variables
        _key = key
        _name = name
        def __init__(self, **kwargs):
            for variable in Packet._variables:
                setattr(self, variable.name, kwargs.get(variable.name, variable.default))

    for enum in enums:
        setattr(Packet, enum.name, enum.enum)

    _lookup_table[key] = Packet

    Packet.__name__ = name
    Packet.__qualname__ = name
    return Packet

def _build_unknown_packet(key):
    _UnknownPacket = _TASDPacketFactory(f"UnknownPacket_{key:04x}", key, [ _VariableDefinition("data", _VariableType.BYTES_EOP, b"") ])
    return _UnknownPacket

def lookup_packet(key: int) -> _TASDPacket:
    packet = _lookup_table.get(key, None)
    if packet == None:
        packet = _build_unknown_packet(key)
    return packet
    