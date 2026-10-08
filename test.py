import struct

with open("normal.wav", "rb") as f:
    b = bytearray(f.read())

original = struct.unpack_from("<I", b, 4)[0]

struct.pack_into("<I", b, 4, original + 0x100000)

with open("poc_riff_size.wav", "wb") as f:
    f.write(b)

print("Original RIFF size:", original)
print("Modified RIFF size:", original + 0x100000)