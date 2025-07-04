import argparse
from clipcode.exporter import export_files_to_clipboard

def main():
    parser = argparse.ArgumentParser(
        description="Exportiert rekursiv alle Dateien mit bestimmten Endungen als Markdown-Codeblöcke in die Zwischenablage."
    )
    parser.add_argument("path", help="Pfad zum Wurzelverzeichnis (z. B. ./src)")
    parser.add_argument(
        "extensions",
        nargs="*",
        help="Liste von Dateiendungen ohne Punkt (z. B. py ts sh). Wenn leer, werden alle Dateien berücksichtigt."
    )
    
    # Gitignore-Optionen
    gitignore_group = parser.add_mutually_exclusive_group()
    gitignore_group.add_argument(
        "--respect-gitignore",
        action="store_true",
        default=True,
        help="Respektiert .gitignore-Dateien und schließt entsprechende Dateien aus (Standard)"
    )
    gitignore_group.add_argument(
        "--no-respect-gitignore",
        action="store_true",
        help="Ignoriert .gitignore-Dateien und inkludiert alle Dateien (außer .git-Ordner)"
    )

    args = parser.parse_args()
    extensions = args.extensions if args.extensions else None
    respect_gitignore = not args.no_respect_gitignore
    export_files_to_clipboard(args.path, extensions, respect_gitignore)
