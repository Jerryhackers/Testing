import struct
import sys
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else "normal.wav")
dst = Path("malformed.wav")

buf = bytearray(src.read_bytes())

# RIFF/WAVE sanity check
if len(buf) < 12 or buf[0:4] != b"RIFF" or buf[8:12] != b"WAVE":
    raise SystemExit("Not a standard RIFF/WAVE file")

# Locate the data chunk
pos = 12
data_chunk = None

while pos + 8 <= len(buf):
    chunk_id = bytes(buf[pos:pos + 4])
    chunk_size = struct.unpack_from("<I", buf, pos + 4)[0]

    if chunk_id == b"data":
        data_chunk = pos
        break

    # RIFF chunks are word-aligned
    pos += 8 + chunk_size
    if chunk_size & 1:
        pos += 1

if data_chunk is None:
    raise SystemExit("data chunk not found")

old_size = struct.unpack_from("<I", buf, data_chunk + 4)[0]

# Claim that the data chunk is much larger than the bytes
# actually present in the file.
new_size = old_size + 0x100000

struct.pack_into("<I", buf, data_chunk + 4, new_size)

dst.write_bytes(buf)

print(f"[+] Input:          {src}")
print(f"[+] Output:         {dst}")
print(f"[+] Original size:  0x{old_size:08X} ({old_size})")
print(f"[+] Declared size:  0x{new_size:08X} ({new_size})")
print("[+] Actual file bytes were NOT enlarged.")