#!/usr/bin/env python3
"""inventory.py 테스트"""
import sys
from pathlib import Path

import pytest

import inventory


@pytest.mark.parametrize(
    "size, expected",
    [
        (0, "0.0 B"),
        (1, "1.0 B"),
        (1023, "1023.0 B"),
        (1024, "1.0 KB"),
        (1536, "1.5 KB"),
        (1024 ** 2, "1.0 MB"),
        (1024 ** 3, "1.0 GB"),
        (1024 ** 4, "1.0 TB"),
    ],
)
def test_human_size(size, expected):
    assert inventory.human_size(size) == expected


def test_main_lists_files(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.txt").write_text("hello")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "b.bin").write_bytes(b"x" * 2048)

    monkeypatch.setattr(sys, "argv", ["inventory.py", str(tmp_path)])
    inventory.main()

    out = capsys.readouterr().out
    assert "| a.txt | 5.0 B |" in out
    assert "| sub/b.bin | 2.0 KB |" in out
    assert "총 2개" in out


def test_main_skips_hidden_files(tmp_path, monkeypatch, capsys):
    (tmp_path / "visible.txt").write_text("ok")
    (tmp_path / ".hidden").write_text("nope")
    hidden_dir = tmp_path / ".git"
    hidden_dir.mkdir()
    (hidden_dir / "config").write_text("nope")

    monkeypatch.setattr(sys, "argv", ["inventory.py", str(tmp_path)])
    inventory.main()

    out = capsys.readouterr().out
    assert "visible.txt" in out
    assert ".hidden" not in out
    assert ".git" not in out
    assert "총 1개" in out
