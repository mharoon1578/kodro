"""Tests for utility functions."""

from __future__ import annotations

from pathlib import Path

from kodro.utils import (
    calculate_cost,
    chunk_text,
    parse_checkbox_tasks,
    parse_xml_files,
    write_file,
)


def test_parse_checkbox_tasks() -> None:
    md = """
- [ ] Task A
- [x] Task B
- [ ] [P] Parallel Task C
- [X] [p] Parallel Done D
"""
    tasks = parse_checkbox_tasks(md)
    assert len(tasks) == 4
    assert tasks[0]["description"] == "Task A"
    assert tasks[0]["completed"] is False
    assert tasks[0]["parallel"] is False
    assert tasks[2]["parallel"] is True
    assert tasks[2]["description"] == "Parallel Task C"
    assert tasks[3]["completed"] is True


def test_parse_xml_files() -> None:
    xml = '''
<file path="src/main.py">
print("hello")
</file>
<file path="README.md">
# Hello
</file>
'''
    files = parse_xml_files(xml)
    assert len(files) == 2
    assert files[0]["path"] == "src/main.py"
    assert 'print("hello")' in files[0]["content"]


def test_write_file_atomic(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "file.txt"
    write_file(target, "atomic content")
    assert target.exists()
    assert target.read_text(encoding="utf-8") == "atomic content"



def test_calculate_cost() -> None:
    cost = calculate_cost("gpt-4o", 1000, 500)
    assert cost > 0
    assert cost == 0.0125


def test_chunk_text_by_sections() -> None:
    text = "## Section A\n" + "x " * 1000 + "\n## Section B\n" + "y " * 500
    chunks = chunk_text(text, max_chars=500)
    assert len(chunks) >= 2
    assert any("Section A" in c for c in chunks)
    assert any("Section B" in c for c in chunks)
