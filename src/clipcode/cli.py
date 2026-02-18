import argparse
from clipcode.exporter import export_files_to_clipboard


def _parse_truncate_lines(value: str, parser: argparse.ArgumentParser) -> tuple[int, int]:
    parts = value.split(":")
    if len(parts) != 2:
        parser.error("--truncate-lines muss das Format KÜRZENAB:KÜRZENAUF haben (z. B. 3000:500).")

    try:
        truncate_from = int(parts[0])
        truncate_to = int(parts[1])
    except ValueError:
        parser.error("--truncate-lines erwartet ganze Zahlen im Format KÜRZENAB:KÜRZENAUF.")

    if truncate_from < 0 or truncate_to < 0:
        parser.error("--truncate-lines erlaubt keine negativen Werte.")

    if truncate_to > truncate_from:
        parser.error("Bei --truncate-lines muss KÜRZENAUF kleiner oder gleich KÜRZENAB sein.")

    return truncate_from, truncate_to

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
    
    # Explizite Ignore-Patterns
    parser.add_argument(
        "-i", "--ignore",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Pfad- oder Glob-Muster explizit ignorieren (mehrfach verwendbar oder als Kommaliste)."
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

    parser.add_argument(
        "--truncate-lines",
        default="3000:500",
        metavar="KÜRZENAB:KÜRZENAUF",
        help=(
            "Große Dateien ab KÜRZENAB Zeilen kürzen oder ignorieren. "
            "Beispiel: 3000:500 (Standard), 3000:0 = ignorieren."
        ),
    )

    args = parser.parse_args()
    extensions = args.extensions if args.extensions else None
    respect_gitignore = not args.no_respect_gitignore
    truncate_from, truncate_to = _parse_truncate_lines(args.truncate_lines, parser)

    # Alle Ignore-Argumente in eine Liste von Mustern umwandeln
    ignore_patterns: list[str] = []
    for item in args.ignore:
        ignore_patterns.extend([p.strip() for p in item.split(",") if p.strip()])

    export_files_to_clipboard(
        args.path,
        extensions,
        respect_gitignore,
        ignore_patterns,
        truncate_from,
        truncate_to,
    )
