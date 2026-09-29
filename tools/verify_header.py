#!/usr/bin/env python3
"""核對挖洞產出的檔頭。

第 3 行必須是「第 4 行起到檔尾」原始位元組的 SHA-256（小寫十六進位）。
相符印 OK、離開碼 0；不符印 MISMATCH、離開碼 1。
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def split_header(data: bytes) -> tuple[str, bytes] | None:
    """回傳 (第 3 行宣告, 第 4 行起的原始位元組)。少於 4 行則回傳 None。"""
    marks: list[int] = []
    for index, byte in enumerate(data):
        if byte == 0x0A:
            marks.append(index)
            if len(marks) == 3:
                break
    if len(marks) < 3:
        return None
    line3 = data[marks[1] + 1 : marks[2]].strip()
    try:
        declared = line3.decode("ascii").lower()
    except UnicodeDecodeError:
        declared = ""
    body = data[marks[2] + 1 :]
    return declared, body


def check(data: bytes) -> bool:
    parsed = split_header(data)
    if parsed is None:
        return False
    declared, body = parsed
    actual = hashlib.sha256(body).hexdigest()
    return bool(_HEX64.fullmatch(declared) and declared == actual)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python tools/verify_header.py <file>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        data = path.read_bytes()
    except OSError as exc:
        print(f"cannot read {path}: {exc}", file=sys.stderr)
        return 2
    if check(data):
        print("OK")
        return 0
    print("MISMATCH")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
