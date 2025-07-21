import subprocess
import os
from clipcode.file_utils import find_files_with_extensions, read_file_content, find_all_files
from clipcode.syntax import get_syntax_highlight_tag
from clipcode.gitignore_utils import filter_files_by_gitignore
import fnmatch
from pathlib import Path

def export_files_to_clipboard(
    root_path: str,
    extensions: list[str] | None,
    respect_gitignore: bool = True,
    ignore_patterns: list[str] | None = None,
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
        content = read_file_content(file_path)
        lang = get_syntax_highlight_tag(file_path)
        output.append(f"### {file_path}\n```{lang}\n{content}\n```\n---\n")

    formatted_result = '\n'.join(output)

    try:
        subprocess.run(["wl-copy"], input=formatted_result.encode(), check=True)
        print("✅ Inhalt erfolgreich in die Zwischenablage kopiert.")
    except Exception as e:
        print(f"❌ Fehler beim Kopieren in die Zwischenablage: {e}")
