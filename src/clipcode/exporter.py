import subprocess
import os
from clipcode.file_utils import find_files_with_extensions, read_file_content, find_all_files
from clipcode.syntax import get_syntax_highlight_tag
from clipcode.gitignore_utils import filter_files_by_gitignore
import fnmatch
from pathlib import Path


def _should_skip_file_for_export(file_path: str) -> bool:
    # Skip SVG explicitly (even though it's text, it can be large/noisy for clipboard exports)
    if Path(file_path).suffix.lower() == ".svg":
        return True

    try:
        with open(file_path, "rb") as f:
            chunk = f.read(4096)
    except OSError:
        # If we can't read it, treat it as non-exportable for safety.
        return True

    if not chunk:
        return False

    # Fast binary indicator
    if b"\x00" in chunk:
        return True

    # Heuristic: count non-text bytes
    text_bytes = set(b"\t\n\r\f\b") | set(range(0x20, 0x7F))
    non_text = sum(byte not in text_bytes for byte in chunk)
    return (non_text / len(chunk)) > 0.30

def export_files_to_clipboard(
    root_path: str,
    extensions: list[str] | None,
    respect_gitignore: bool = True,
    ignore_patterns: list[str] | None = None,
    truncate_from: int = 3000,
    truncate_to: int = 500,
):
    if extensions is None:
        # Wenn extensions None ist, alle Dateien finden
        files = find_all_files(root_path)
    else:
        files = find_files_with_extensions(root_path, extensions)

    # Immer .git-Ordner und .gitignore-Dateien ausschließen
    files = [f for f in files if '.git' not in Path(f).parts and Path(f).name != '.gitignore']

    # Explizite Ignore-Patterns anwenden (höchste Priorität)
    if ignore_patterns:
        def _matches_ignore(patterns: list[str], file_path: str) -> bool:
            path_posix = file_path.replace(os.sep, '/')
            return any(
                fnmatch.fnmatch(path_posix, pat) or fnmatch.fnmatch(Path(file_path).name, pat)
                for pat in patterns
            )
        files = [f for f in files if not _matches_ignore(ignore_patterns, f)]

    # Gitignore-Filterung anwenden, falls aktiviert
    if respect_gitignore:
        files = filter_files_by_gitignore(files, root_path)

    output = []
    output.append("## Projektdateien\n")

    for file_path in files:
        if _should_skip_file_for_export(file_path):
            continue
        content = read_file_content(file_path)
        lines = content.splitlines()
        line_count = len(lines)

        if line_count > truncate_from:
            if truncate_to == 0:
                continue
            content = "\n".join(lines[:truncate_to])

        lang = get_syntax_highlight_tag(file_path)
        file_output = [f"### {file_path}\n```{lang}\n{content}\n```\n"]
        if line_count > truncate_from and truncate_to > 0:
            file_output.append(
                f"⚠️ Datei gekürzt: {line_count} → {truncate_to} Zeilen (Grenze: > {truncate_from}).\n"
            )
        file_output.append("---\n")
        output.append("".join(file_output))

    formatted_result = '\n'.join(output)

    try:
        subprocess.run(["wl-copy"], input=formatted_result.encode(), check=True)
        print("✅ Inhalt erfolgreich in die Zwischenablage kopiert.")
    except Exception as e:
        print(f"❌ Fehler beim Kopieren in die Zwischenablage: {e}")
