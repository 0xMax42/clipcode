import subprocess
import os
from clipcode.file_utils import find_files_with_extensions, read_file_content, find_all_files
from clipcode.syntax import get_syntax_highlight_tag

def export_files_to_clipboard(root_path: str, extensions: list[str] | None):
    if extensions is None:
        # Wenn extensions None ist, alle Dateien finden
        files = find_all_files(root_path)
    else:
        files = find_files_with_extensions(root_path, extensions)

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
