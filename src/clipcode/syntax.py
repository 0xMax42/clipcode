import os

def get_syntax_highlight_tag(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    return {
        ".sh": "bash",
        ".py": "python",
        ".ts": "ts",
        ".js": "javascript",
        ".json": "json",
        ".html": "html",
        ".css": "css",
        ".md": "markdown",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".ini": "ini",
        ".c": "c",
        ".cpp": "cpp",
        ".rs": "rust",
    }.get(ext, "")
