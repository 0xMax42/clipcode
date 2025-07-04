# 📋 clipcode

**clipcode** ist ein minimalistisches, aber leistungsfähiges CLI-Tool zur Extraktion von Quellcodedateien in ein Markdown-kompatibles Format – ideal zur Verwendung in Prompts für ChatGPT & Co.
Es exportiert rekursiv Dateien mit bestimmten Endungen und kopiert sie als sauber strukturierte Markdown-Datei direkt in die Zwischenablage.

---

## 🚀 Features

* 🔎 Rekursive Suche nach Quelldateien anhand beliebiger Endungen
* 📃 Ausgabe als Markdown mit Syntax-Highlighting (z. B. `python`, `bash`)
* 🔹 Kopiert die formatierte Ausgabe direkt ins Clipboard (Wayland via `wl-copy`)
* ✨ Ideal zur Prompt-Erzeugung für LLMs wie ChatGPT / GPT-4o
* 🚀 Extrem schnell, keine Abhängigkeiten außerhalb der Standardbibliothek
* 🚫 **Intelligente .gitignore-Unterstützung** – respektiert automatisch .gitignore-Dateien
* 🔒 **Automatischer .git-Ausschluss** – .git-Ordner werden immer ausgeschlossen
* ⚙️ **Konfigurierbar** – gitignore-Respekt kann deaktiviert werden

---

## ⚙️ Installation

### 📦 Installation (empfohlen)

```bash
poetry install
poetry run clipcode ./src py ts sh
```

### oder global installieren (dev)

```bash
poetry build
pip install dist/clipcode-*.whl
clipcode ./src py ts sh
```

---

## 🔀 Verwendung

```bash
clipcode [optionen] <pfad> [<endung> ...]
```

### Grundlegende Beispiele

```bash
# Alle Python- und TypeScript-Dateien
clipcode ./src py ts

# Alle Dateien (respektiert .gitignore)
clipcode ./src

# Spezifische Dateitypen mit .gitignore-Respekt (Standard)
clipcode ./src py ts sh toml
```

### .gitignore-Optionen

```bash
# Standard: .gitignore wird respektiert
clipcode ./src py ts

# Explizit .gitignore respektieren
clipcode --respect-gitignore ./src py ts

# .gitignore ignorieren (nur .git-Ordner wird ausgeschlossen)
clipcode --no-respect-gitignore ./src py ts
```

### Ergebnis (im Clipboard):

````markdown
## Projektdateien

### ./src/main.py
```python
# ... dein Code hier ...
```
````

## 🚫 .gitignore-Unterstützung

**clipcode** respektiert standardmäßig `.gitignore`-Dateien und schließt entsprechende Dateien automatisch aus der Ausgabe aus.

### Unterstützte .gitignore-Features:
- ✅ **Wildcards**: `*.log`, `*.tmp`, `test_*`
- ✅ **Verzeichnis-Patterns**: `__pycache__/`, `node_modules/`
- ✅ **Pfad-spezifische Patterns**: `src/*.tmp`, `/build`
- ✅ **Negation**: `!important.log` (Ausnahmen definieren)
- ✅ **Kommentare**: `# Dies ist ein Kommentar`
- ✅ **Hierarchische .gitignore**: Unterstützt mehrere .gitignore-Dateien in der Verzeichnisstruktur

### Immer ausgeschlossen:
- 🔒 `.git/` Ordner (unabhängig von Optionen)
- 📄 `.gitignore` Dateien selbst

### Beispiel .gitignore:
```gitignore
# Logs
*.log
debug.txt

# Compiled files
__pycache__/
*.pyc
*.pyo

# Build directories
/build
/dist

# IDE files
.vscode/
.idea/

# Ausnahme für wichtige Dateien
!important.log
```

---

## 📁 Projektstruktur

```text
clipcode/
├── cli.py              # Argument-Parsing, Einstiegspunkt
├── exporter.py         # Clipboard-Export und Markdown-Formatierung
├── file_utils.py       # Dateisuche und Inhaltseinlesung
├── gitignore_utils.py  # .gitignore-Parser und Filterlogik
├── syntax.py           # Zuordnung von Dateiendungen zu Markdown-Sprachen
├── __main__.py         # Poetry CLI Entry Point
└── __init__.py
```

---

## 💡 Hinweise

* Clipboard-Funktion basiert aktuell auf `wl-copy` (Wayland)
* Weitere Clipboard-Backends sind leicht integrierbar
* Vollständige .gitignore-Unterstützung implementiert
* Alle Tests bestehen erfolgreich (22 umfassende Tests)

---

## ✍️ Lizenz

MIT License — siehe [LICENSE](./LICENSE)

---

## 📊 Autor

**Max P.** • [0xMax42.io](https://0xmax42.io)
