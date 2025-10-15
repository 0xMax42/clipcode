import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest


def _make_temp_dir():
    tmp = tempfile.mkdtemp()
    return Path(tmp)


def test_filter_with_relative_paths_should_respect_gitignore():
    """
    Repro: Wenn Dateien relativ sind (wie bei `clipcode .`) und root_path='.',
    dann sollte .gitignore im aktuellen Verzeichnis dennoch greifen.

    Aktueller Bug: target/* bleibt erhalten.
    Dieser Test drückt das erwartete (korrekte) Verhalten aus und SOLL aktuell fehlschlagen.
    """
    # Lazy import to avoid PYTHONPATH issues at collection time
    from clipcode.file_utils import find_all_files
    from clipcode.gitignore_utils import filter_files_by_gitignore

    temp = _make_temp_dir()
    try:
        # Projektstruktur anlegen
        (temp / "target").mkdir(parents=True, exist_ok=True)
        (temp / "src").mkdir(parents=True, exist_ok=True)
        (temp / "src" / "main.rs").write_text("fn main() {}\n", encoding="utf-8")
        # .gitignore im Projekt-Root
        (temp / ".gitignore").write_text("/target/\n*.rlib\n", encoding="utf-8")
        # Build-Artefakt
        (temp / "target" / "foo.rlib").write_text("bin", encoding="utf-8")

        # In das Verzeichnis wechseln und relativ arbeiten (wie `clipcode .`)
        cwd_before = Path.cwd()
        os.chdir(temp)
        try:
            files = find_all_files(".")  # liefert relative Pfade
            filtered = filter_files_by_gitignore(files, ".")

            # Erwartung: nichts aus target/* darf enthalten sein
            assert all(
                not (p.startswith("target/") or p.startswith("./target/")) for p in filtered
            ), "target-Dateien dürfen nicht enthalten sein"
        finally:
            os.chdir(cwd_before)
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp)


def test_cli_with_dot_should_respect_gitignore_in_cwd():
    """
    Repro über CLI: `clipcode .` im Projektverzeichnis mit .gitignore '/target/'.

    Erwartung: target/* wird nicht in den Clipboard-Output aufgenommen.
    Aktuell: target/* wird aufgenommen (Bug). Dieser Test soll derzeit FAILen.
    """
    from clipcode.cli import main as cli_main

    temp = _make_temp_dir()
    try:
        # Projektstruktur
        (temp / "target").mkdir(parents=True, exist_ok=True)
        (temp / "src").mkdir(parents=True, exist_ok=True)
        (temp / "src" / "main.rs").write_text("fn main() {}\n", encoding="utf-8")
        (temp / ".gitignore").write_text("/target/\n*.rlib\n", encoding="utf-8")
        (temp / "target" / "foo.rlib").write_text("bin", encoding="utf-8")

        # In temp wechseln und CLI mit '.' aufrufen
        cwd_before = Path.cwd()
        os.chdir(temp)
        try:
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock()
                with patch.object(sys, "argv", ["clipcode", "."]):
                    cli_main()

                # Clipboard-Inhalt prüfen
                clipboard_content = mock_run.call_args[1]["input"].decode("utf-8")
                assert "target/" not in clipboard_content
                assert "foo.rlib" not in clipboard_content
        finally:
            os.chdir(cwd_before)
    finally:
        import shutil
        shutil.rmtree(temp)
