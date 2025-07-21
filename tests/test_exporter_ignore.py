import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from clipcode.exporter import export_files_to_clipboard


class TestExporterIgnorePatterns(unittest.TestCase):
    """Tests für die explicit ignore-Option im Exporter."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def _create_file(self, relative_path: str, content: str = "data"):
        file_path = self.temp_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return file_path

    @patch("subprocess.run")
    def test_ignore_patterns_exclude_files(self, mock_run):
        """Stellt sicher, dass Dateien, die durch -i/--ignore angegeben sind, ausgeschlossen werden."""
        # Dateien erstellen
        keep_py = self._create_file("keep.py", "print('keep')")
        ignore_py = self._create_file("ignore_me.py", "print('ignore')")
        log_file = self._create_file("logs/app.log", "log")

        # Clipboard Call abfangen
        mock_run.return_value = MagicMock()

        export_files_to_clipboard(
            root_path=str(self.temp_path),
            extensions=None,
            respect_gitignore=False,
            ignore_patterns=["ignore_me.py", "*.log"],
        )

        # Inhalt aus dem Clipboard-Aufruf extrahieren
        call_args = mock_run.call_args
        clipboard_content = call_args[1]["input"].decode("utf-8")

        self.assertIn("keep.py", clipboard_content)
        self.assertNotIn("ignore_me.py", clipboard_content)
        self.assertNotIn("app.log", clipboard_content)

    @patch("subprocess.run")
    def test_ignore_patterns_override_gitignore_negation(self, mock_run):
        """Explizite Patterns haben Vorrang vor .gitignore-Negationen."""
        # Dateien anlegen
        overridden_file = self._create_file("important.py", "print('important')")
        # .gitignore mit Negation (!important.py) – würde die Datei eigentlich erzwingen
        (self.temp_path / ".gitignore").write_text("*.py\n!important.py\n", encoding="utf-8")

        mock_run.return_value = MagicMock()

        export_files_to_clipboard(
            root_path=str(self.temp_path),
            extensions=None,
            respect_gitignore=True,
            ignore_patterns=["important.py"],
        )

        clipboard_content = mock_run.call_args[1]["input"].decode("utf-8")

        # Trotz Negation soll Datei ausgeschlossen werden
        self.assertNotIn("important.py", clipboard_content)


if __name__ == "__main__":
    unittest.main()
