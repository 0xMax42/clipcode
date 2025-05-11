# 📋 clipcode

**clipcode** ist ein minimalistisches, aber leistungsfähiges CLI-Tool zur Extraktion von Quellcodedateien in ein Markdown-kompatibles Format – ideal zur Verwendung in Prompts für ChatGPT & Co.
Es exportiert rekursiv Dateien mit bestimmten Endungen und kopiert sie als sauber strukturierte Markdown-Datei direkt in die Zwischenablage.

---

## 🚀 Features

* 🔎 Rekursive Suche nach Quelldateien anhand beliebiger Endungen
* 📃 Ausgabe als Markdown mit Syntax-Highlighting (z. B. `python`, `bash`)
* 🔹 Kopiert die formatierte Ausgabe direkt ins Clipboard (Wayland via `wl-copy`)
* ✨ Ideal zur Prompt-Erzeugung für LLMs wie ChatGPT / GPT-4o
* 🚀 Extrem schnell, keine Abhängigkeiten außerhalb der Standardbibliothek

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
clipcode <pfad> <endung> [<endung> ...]
```

### Beispiel

```bash
clipcode ./src py ts sh toml
```

Dies erzeugt eine Markdown-Ausgabe aller `.py`, `.ts`, `.sh` und `.toml` Dateien unterhalb von `./src`, formatiert mit Syntax-Hervorhebung, und kopiert sie ins Clipboard.

### Ergebnis (im Clipboard):

````markdown
## Projektdateien

### ./src/main.py
```python
# ... dein Code hier ...
```
````

---

## 📁 Projektstruktur

```text
clipcode/
├── cli.py           # Argument-Parsing, Einstiegspunkt
├── exporter.py      # Clipboard-Export und Markdown-Formatierung
├── file_utils.py    # Dateisuche und Inhaltseinlesung
├── syntax.py        # Zuordnung von Dateiendungen zu Markdown-Sprachen
├── __main__.py      # Poetry CLI Entry Point
└── __init__.py
```

---

## 💡 Hinweise

* Clipboard-Funktion basiert aktuell auf `wl-copy` (Wayland)
* Weitere Clipboard-Backends sind leicht integrierbar
* `.clipcodeignore` ist geplant (analog zu `.gitignore`)

---

## ✍️ Lizenz

MIT License — siehe [LICENSE](./LICENSE)

---

## 📊 Autor

**Max P.** • [0xMax42.io](https://0xmax42.io)
