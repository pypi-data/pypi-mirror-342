import tasd.packets as packets
import tasd.constants as constants
import tasd.utils as utils
from tasd.packet import lookup_packet, _TASDPacket
from typing import List

class TASD():
    MAGIC = b"TASD"
    def __init__(self, version = 1, g_keylen = 2):
        self.version = version
        self.g_keylen = g_keylen
        self.packets: List[_TASDPacket] = []
    @classmethod
    def from_bytes(cls, buffer: bytes, *, bypass_errors = False):
        magic = utils.readBytes(buffer, 0, 4)
        if magic != cls.MAGIC:
            raise ValueError("Invalid TASD File, Missing Magic")
        version = utils.readUint16(buffer, 4)
        if version != 1 and not bypass_errors:
            raise ValueError("Unsupported TASD File, Version Unsupported", version)
        g_keylen = utils.readUint8(buffer, 6)
        if g_keylen != 2:
            raise ValueError("Unsupported TASD File, Unknown G_KEYLEN", g_keylen)
        self = cls(version, g_keylen)
        index = 7
        while index < len(buffer):
            key = utils.readUintN(buffer, index, self.g_keylen)
            index += self.g_keylen
            packet_cls = lookup_packet(key)
            pexp = utils.readUint8(buffer, index)
            index += 1
            plen = utils.readUintN(buffer, index, pexp)
            index += pexp
            data = utils.readBytes(buffer, index, plen)
            index += plen
            packet = packet_cls.from_bytes(data)
            self.packets.append(packet)
        return self
    def to_bytes(self):
        header = bytearray(7)
        header[0:4] = self.MAGIC
        utils.writeUint16(self.version, header, 4)
        utils.writeUint8(self.g_keylen, header, 6)
        packets = [ header ]
        for packet in self.packets:
            plen = packet.size()
            pexp = utils.minUint(plen)
            size = self.g_keylen + 1 + pexp
            buffer = bytearray(size)
            utils.writeUintN(packet._key, buffer, 0, self.g_keylen)
            utils.writeUint8(pexp, buffer, self.g_keylen)
            utils.writeUintN(plen, buffer, self.g_keylen + 1, pexp)
            payload = packet.to_bytes()
            packets.append(buffer + payload)
        return b"".join(packets)
    def __repr__(self):
        return f"TASD(version={self.version}, g_keylen={self.g_keylen})"
