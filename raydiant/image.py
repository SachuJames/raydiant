"""Tiny image writers. PNG is hand encoded with zlib and struct, no deps."""

from __future__ import annotations

import struct
import zlib


def write_ppm(path: str, width: int, height: int, rows) -> None:
    with open(path, "w") as f:
        f.write(f"P3\n{width} {height}\n255\n")
        for row in rows:
            for (r, g, b) in row:
                f.write(f"{r} {g} {b}\n")


def _chunk(tag: bytes, data: bytes) -> bytes:
    out = struct.pack(">I", len(data)) + tag + data
    out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return out


def write_png(path: str, width: int, height: int, rows) -> None:
    raw = bytearray()
    for row in rows:
        raw.append(0)  # filter type 0: no filtering
        for (r, g, b) in row:
            raw += bytes((r, g, b))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(_chunk(b"IHDR", ihdr))
        f.write(_chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        f.write(_chunk(b"IEND", b""))
