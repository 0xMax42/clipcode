import os

def find_files_with_extensions(root_path: str, extensions: list[str]) -> list[str]:
    matches = []
    normalized_exts = {f".{ext.lower()}" for ext in extensions}
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in normalized_exts):
                matches.append(os.path.join(dirpath, filename))
    return matches

def read_file_content(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='latin1') as file:
            return file.read()
    except Exception as e:
        return f"[Fehler beim Lesen der Datei: {e}]"

def find_all_files(root_path: str) -> list[str]:
    """Findet alle Dateien rekursiv ab dem angegebenen Wurzelverzeichnis."""
    matches = []
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            matches.append(os.path.join(dirpath, filename))
    return matches
