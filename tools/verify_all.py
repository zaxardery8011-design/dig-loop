#!/usr/bin/env python3
"""對一個資料夾內每個 *.md 做與 verify_header 相同的檔頭檢查。

逐檔印 OK 或 MISMATCH。全部 OK 才離開碼 0；有任一不符離開碼 1。
"""

from __future__ import annotations

import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from verify_header import check


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python tools/verify_all.py <dir>", file=sys.stderr)
        return 2
    folder = Path(argv[1])
    if not folder.is_dir():
        print(f"not a directory: {folder}", file=sys.stderr)
        return 2
    files = sorted(folder.glob("*.md"), key=lambda path: path.name.lower())
    if not files:
        print(f"no *.md in {folder}", file=sys.stderr)
        return 2
    ok = True
    for path in files:
        try:
            data = path.read_bytes()
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if check(data):
            print(f"OK {path.name}")
        else:
            print(f"MISMATCH {path.name}")
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
