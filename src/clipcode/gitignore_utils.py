import os
import fnmatch
from pathlib import Path
from typing import List, Set


class GitignoreParser:
    """Parser für .gitignore-Dateien mit Unterstützung für Standard-gitignore-Patterns."""
    
    def __init__(self, gitignore_path: str):
        self.gitignore_path = Path(gitignore_path)
        self.base_dir = self.gitignore_path.parent
        self.patterns = []
        self._parse_gitignore()
    
    def _parse_gitignore(self):
        """Parst die .gitignore-Datei und extrahiert die Patterns."""
        if not self.gitignore_path.exists():
            return
        
        try:
            with open(self.gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Ignoriere leere Zeilen und Kommentare
                    if not line or line.startswith('#'):
                        continue
                    
                    # Behandle Negation
                    negated = line.startswith('!')
                    if negated:
                        line = line[1:]
                    
                    self.patterns.append({
                        'pattern': line,
                        'negated': negated,
                        'is_dir': line.endswith('/')
                    })
        except Exception:
            # Bei Fehlern beim Lesen der .gitignore-Datei, ignoriere sie
            pass
    
    def is_ignored(self, file_path: str) -> bool:
        """Prüft, ob eine Datei/Verzeichnis von den gitignore-Patterns ignoriert wird."""
        file_path_obj = Path(file_path)
        
        # Konvertiere zu relativem Pfad bezogen auf das .gitignore-Verzeichnis
        try:
            rel_path = file_path_obj.relative_to(self.base_dir)
        except ValueError:
            # Datei ist nicht im Bereich dieser .gitignore
            return False
        
        rel_path_str = str(rel_path)
        rel_path_posix = rel_path_str.replace(os.sep, '/')
        
        ignored = False
        
        for pattern_info in self.patterns:
            pattern = pattern_info['pattern']
            is_dir_pattern = pattern_info['is_dir']
            negated = pattern_info['negated']
            
            # Entferne trailing slash für Verzeichnis-Patterns
            if is_dir_pattern:
                pattern = pattern.rstrip('/')
            
            matched = False
            
            # Verschiedene Matching-Strategien
            if '/' in pattern:
                # Pattern enthält Pfad-Separatoren
                if pattern.startswith('/'):
                    # Absoluter Pfad vom Repository-Root
                    pattern = pattern[1:]
                    matched = fnmatch.fnmatch(rel_path_posix, pattern)
                    # Auch für Verzeichnisse: teste ob der Pfad mit dem Pattern beginnt
                    if not matched and rel_path_posix.startswith(pattern):
                        matched = True
                else:
                    # Relativer Pfad
                    matched = fnmatch.fnmatch(rel_path_posix, pattern)
                    # Auch gegen alle Teilpfade testen
                    if not matched:
                        path_parts = rel_path_posix.split('/')
                        for i in range(len(path_parts)):
                            subpath = '/'.join(path_parts[i:])
                            if fnmatch.fnmatch(subpath, pattern):
                                matched = True
                                break
            else:
                # Einfacher Dateiname/Pattern
                matched = fnmatch.fnmatch(rel_path.name, pattern)
                # Auch gegen den vollständigen Pfad testen
                if not matched:
                    matched = fnmatch.fnmatch(rel_path_posix, pattern)
                # Teste gegen alle Pfad-Komponenten
                if not matched:
                    path_parts = rel_path_posix.split('/')
                    for part in path_parts:
                        if fnmatch.fnmatch(part, pattern):
                            matched = True
                            break
            
            # Für Verzeichnis-Patterns: nur matchen wenn es ein Verzeichnis ist
            if matched and is_dir_pattern and file_path_obj.is_file():
                # Prüfe ob ein übergeordnetes Verzeichnis matched
                parent_matched = False
                for parent in file_path_obj.parents:
                    try:
                        parent_rel = parent.relative_to(self.base_dir)
                        parent_rel_posix = str(parent_rel).replace(os.sep, '/')
                        if fnmatch.fnmatch(parent_rel_posix, pattern):
                            parent_matched = True
                            break
                    except ValueError:
                        break
                matched = parent_matched
            
            if matched:
                if negated:
                    ignored = False
                else:
                    ignored = True
        
        return ignored


def find_gitignore_files(start_path: str) -> List[str]:
    """Findet alle .gitignore-Dateien vom Startpfad bis zur Wurzel."""
    gitignore_files = []
    current_path = Path(start_path).resolve()
    
    while True:
        gitignore_path = current_path / '.gitignore'
        if gitignore_path.exists():
            gitignore_files.append(str(gitignore_path))
        
        parent = current_path.parent
        if parent == current_path:  # Wurzel erreicht
            break
        current_path = parent
    
    return gitignore_files


def should_ignore_file(file_path: str, gitignore_files: List[str]) -> bool:
    """Prüft, ob eine Datei von einer der .gitignore-Dateien ignoriert werden soll."""
    file_path_obj = Path(file_path)
    
    # Hardcoded: .git-Ordner immer ausschließen
    if '.git' in file_path_obj.parts:
        return True
    
    # Prüfe gegen alle .gitignore-Dateien
    for gitignore_file in gitignore_files:
        parser = GitignoreParser(gitignore_file)
        if parser.is_ignored(file_path):
            return True
    
    return False


def filter_files_by_gitignore(files: List[str], root_path: str) -> List[str]:
    """Filtert eine Liste von Dateien basierend auf .gitignore-Regeln."""
    # Normalisiere Root- und Dateipfade auf absolute Pfade, damit das Matching konsistent ist
    abs_root = Path(root_path).resolve()
    gitignore_files = find_gitignore_files(str(abs_root))

    filtered_files: List[str] = []
    for file_path in files:
        p = Path(file_path)
        abs_file = p if p.is_absolute() else (abs_root / p).resolve()

        # Immer .git-Ordner ausschließen
        if '.git' in abs_file.parts:
            continue

        # .gitignore-Dateien selbst ausschließen
        if abs_file.name == '.gitignore':
            continue

        # Gitignore-Regeln anwenden, falls vorhanden
        if gitignore_files:
            if not should_ignore_file(str(abs_file), gitignore_files):
                filtered_files.append(str(abs_file))
        else:
            # Keine .gitignore-Dateien vorhanden, Datei einschließen
            filtered_files.append(str(abs_file))

    return filtered_files
