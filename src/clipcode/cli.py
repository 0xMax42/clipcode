import argparse
from clipcode.exporter import export_files_to_clipboard

def main():
    parser = argparse.ArgumentParser(
        description="Exportiert rekursiv alle Dateien mit bestimmten Endungen als Markdown-Codeblöcke in die Zwischenablage."
    )
    parser.add_argument("path", help="Pfad zum Wurzelverzeichnis (z. B. ./src)")
    parser.add_argument(
        "extensions",
        nargs="+",
        help="Liste von Dateiendungen ohne Punkt (z. B. py ts sh)"
    )

    args = parser.parse_args()
    export_files_to_clipboard(args.path, args.extensions)
