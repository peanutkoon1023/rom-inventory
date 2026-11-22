#!/usr/bin/env python3
"""폴더를 스캔해 파일 목록을 마크다운 표로 출력하는 도구"""
import sys
from pathlib import Path

def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    rows = []
    total = 0
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        rows.append((rel, p.stat().st_size))
        total += p.stat().st_size
    print(f"# 목록 — {root}\n")
    print("| 파일 | 크기 |")
    print("|---|---|")
    for rel, size in rows:
        print(f"| {rel} | {human_size(size)} |")
    print(f"\n총 {len(rows)}개 · {human_size(total)}")

if __name__ == "__main__":
    main()
