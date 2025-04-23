def readString(buffer: bytearray, index: int, length: int) -> str:
    return buffer[index:index+length].decode("utf8")
def writeString(string: str, buffer: bytearray, index: int) -> None:
    rawstring = string.encode("utf8")
    buffer[index:index+len(rawstring)] = rawstring
def sizeString(string: str) -> int:
    return len(string.encode("utf8"))

def readBytes(buffer: bytearray, index: int, length: int) -> bytes:
    return buffer[index:index+length]
def writeBytes(value: bytes, buffer: bytearray, index: int) -> None:
    buffer[index:index+len(value)] = value

def readUint8(buffer: bytearray, index: int) -> int:
    return int.from_bytes(buffer[index:index+1], byteorder="big", signed=False)
def readUint16(buffer: bytearray, index: int) -> int:
    return int.from_bytes(buffer[index:index+2], byteorder="big", signed=False)
def readUint24(buffer: bytearray, index: int) -> int:
    return int.from_bytes(buffer[index:index+3], byteorder="big", signed=False)
def readUint32(buffer: bytearray, index: int) -> int:
    return int.from_bytes(buffer[index:index+4], byteorder="big", signed=False)
def readUint64(buffer: bytearray, index: int) -> int:
    return int.from_bytes(buffer[index:index+8], byteorder="big", signed=False)
def readUintN(buffer: bytearray, index: int, size: int) -> int:
    if size == 1:
        return readUint8(buffer, index)
    if size == 2:
        return readUint16(buffer, index)
    if size == 3:
        return readUint24(buffer, index)
    if size == 4:
        return readUint32(buffer, index)
    raise ValueError("Unsuported UintN size", size)

def writeUint8(value: int, buffer: bytearray, index: int) -> None:
    buffer[index:index+1] = (value & (2 ** 8 - 1)).to_bytes(1, byteorder="big", signed=False)
def writeUint16(value: int, buffer: bytearray, index: int) -> None:
    buffer[index:index+2] = (value & (2 ** 16 - 1)).to_bytes(2, byteorder="big", signed=False)
def writeUint24(value: int, buffer: bytearray, index: int) -> None:
    buffer[index:index+3] = (value & (2 ** 24 - 1)).to_bytes(3, byteorder="big", signed=False)
def writeUint32(value: int, buffer: bytearray, index: int) -> None:
    buffer[index:index+4] = (value & (2 ** 32 - 1)).to_bytes(4, byteorder="big", signed=False)
def writeUint64(value: int, buffer: bytearray, index: int) -> None:
    buffer[index:index+8] = (value & (2 ** 64 - 1)).to_bytes(8, byteorder="big", signed=False)
def writeUintN(value: int, buffer: bytearray, index: int, size: int) -> None:
    if size == 1:
        return writeUint8(value, buffer, index)
    if size == 2:
        return writeUint16(value, buffer, index)
    if size == 3:
        return writeUint24(value, buffer, index)
    if size == 4:
        return writeUint32(value, buffer, index)
    raise ValueError("Unsuported UintN size", size)

def minUint(value: int) -> int:
    if value < 256:
        return 1
    if value < 65536:
        return 2
    if value < 16777216:
        return 3
    if value < 4294967296:
        return 4
    raise ValueError("Unsupported UInt size", value);


def readInt8(buffer: bytearray, index: int) -> int:
    return int.from_bytes(buffer[index:index+1], byteorder="big", signed=True)
def readInt16(buffer: bytearray, index: int) -> int:
    return int.from_bytes(buffer[index:index+2], byteorder="big", signed=True)
def readInt24(buffer: bytearray, index: int) -> int:
    return int.from_bytes(buffer[index:index+3], byteorder="big", signed=True)
def readInt32(buffer: bytearray, index: int) -> int:
    return int.from_bytes(buffer[index:index+4], byteorder="big", signed=True)
def readInt64(buffer: bytearray, index: int) -> int:
    return int.from_bytes(buffer[index:index+8], byteorder="big", signed=True)
def readIntN(buffer: bytearray, index: int, n: int) -> int:
    if n == 1:
        return readInt8(buffer, index)
    if n == 2:
        return readInt16(buffer, index)
    if n == 3:
        return readInt24(buffer, index)
    if n == 4:
        return readInt32(buffer, index)
    raise ValueError("Unsuported IntN size", n)

def writeInt8(value: int, buffer: bytearray, index: int) -> None:
    buffer[index:index+1] = (value & (2 ** 8 - 1)).to_bytes(1, byteorder="big", signed=True)
def writeInt16(value: int, buffer: bytearray, index: int) -> None:
    buffer[index:index+2] = (value & (2 ** 16 - 1)).to_bytes(2, byteorder="big", signed=True)
def writeInt24(value: int, buffer: bytearray, index: int) -> None:
    buffer[index:index+3] = (value & (2 ** 24 - 1)).to_bytes(3, byteorder="big", signed=True)
def writeInt32(value: int, buffer: bytearray, index: int) -> None:
    buffer[index:index+4] = (value & (2 ** 32 - 1)).to_bytes(4, byteorder="big", signed=True)
def writeInt64(value: int, buffer: bytearray, index: int) -> None:
    buffer[index:index+8] = (value & (2 ** 64 - 1)).to_bytes(8, byteorder="big", signed=True)
def writeIntN(value: int, buffer: bytearray, index: int, size: int) -> None:
    if size == 1:
        return writeInt8(value, buffer, index)
    if size == 2:
        return writeInt16(value, buffer, index)
    if size == 3:
        return writeInt24(value, buffer, index)
    if size == 4:
        return writeInt32(value, buffer, index)
    raise ValueError("Unsuported IntN size", size)

def minInt(value: int) -> int:
    if -0x80 <= value <= 0x7f:
        return 1
    if -0x8000 <= value <= 0x7fff:
        return 2
    if -0x800000 <= value <= 0x7fffff:
        return 3
    if -0x80000000 <= value <= 0x7fffffff:
        return 4
    raise ValueError("Unsupported Int size", value);

def readBoolean(buffer: bytearray, index: int) -> bool:
    if buffer[index] == 1:
        return True
    if buffer[index] == 0:
        return False
    raise ValueError("Invalid Boolean value")
def writeBoolean(bool: bool, buffer: bytearray, index: int) -> None:
    buffer[index] = (1 if bool else 0)
