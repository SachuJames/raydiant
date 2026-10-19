import struct
import zlib

from raydiant.image import write_png, write_ppm


def _rows(w, h):
    return [[(10, 20, 30)] * w for _ in range(h)]


def test_png_signature_and_ihdr(tmp_path):
    p = tmp_path / "img.png"
    write_png(str(p), 7, 5, _rows(7, 5))
    data = p.read_bytes()

    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    length, tag = struct.unpack(">I4s", data[8:16])
    assert tag == b"IHDR" and length == 13
    width, height, bitdepth, colortype = struct.unpack(">IIBB", data[16:26])
    assert (width, height, bitdepth, colortype) == (7, 5, 8, 2)

    # the image data round trips through the filter bytes we wrote
    idat_start = data.index(b"IDAT") - 4
    idat_len = struct.unpack(">I", data[idat_start:idat_start + 4])[0]
    raw = zlib.decompress(data[idat_start + 8:idat_start + 8 + idat_len])
    assert len(raw) == (1 + 7 * 3) * 5
    assert data.endswith(struct.pack(">I", 0) + b"IEND" + struct.pack(">I", zlib.crc32(b"IEND") & 0xFFFFFFFF))


def test_ppm_header_and_pixels(tmp_path):
    p = tmp_path / "img.ppm"
    write_ppm(str(p), 2, 1, [[(255, 0, 128), (1, 2, 3)]])
    lines = p.read_text().splitlines()
    assert lines[0] == "P3"
    assert lines[1] == "2 1"
    assert lines[2] == "255"
    assert lines[3] == "255 0 128"
    assert lines[4] == "1 2 3"
