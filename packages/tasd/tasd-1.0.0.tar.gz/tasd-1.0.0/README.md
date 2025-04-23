
# TASD

This is a python library for the serialization and deserialization of tasd files using the [tasd file specfication](https://tasd.io/)


## Installation

Install tasd with pip

```bash
  pip install tasd
```
    
## Usage/Examples


Read a file in a print all the packets in it
```py
from tasd import TASD

with open("example.tasd", "rb") as f:
    file = TASD.from_bytes(f.read())

print(file)
for packet in file. packets:
    print(packet)
```

Create a tasd file from scratch and add packets to it
```py
from tasd import TASD, packets

file = TASD()
file.packets.append(packets.extra.Comment(comment="This is a comment"))
file.packets.append(packets.general.Attribution(type=packets.general.Attribution.ATTRIBUTION_TYPE.TASD_FILE_CREATOR, name="Me"))

for packet in file. packets:
    print(packet)

print(file.to_bytes())
```
## Brief API Reference

Not an exhaustive list

`tasd.TASD`

Class holding properties of the tasd file itself: Version and KeyLength

`tasd.constants.PACKET_TYPES`

Enumlike class containing the different packet type indentifiers

`tasd.packets`

Submodule containing all the different packet classes

For details about the different packet types i suggest reading the specification document to determine what packets you need to consider for your use case
## Appendix

Any additional information goes here

