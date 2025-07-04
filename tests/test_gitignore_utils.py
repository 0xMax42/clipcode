import unittest
import tempfile
import os
from pathlib import Path
from clipcode.gitignore_utils import (
    GitignoreParser,
    find_gitignore_files,
    should_ignore_file,
    filter_files_by_gitignore
)


class TestGitignoreParser(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        # Cleanup temp directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_gitignore(self, content: str, path: Path | None = None):
        """Helper method to create a .gitignore file with given content."""
        if path is None:
            path = self.temp_path
        gitignore_path = path / '.gitignore'
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(gitignore_path)
    
    def create_file(self, relative_path: str, content: str = "test content"):
        """Helper method to create a file in the temp directory."""
        file_path = self.temp_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(file_path)
    
    def test_simple_file_pattern(self):
        """Test simple file pattern matching."""
        gitignore_content = "*.log\n*.tmp"
        self.create_gitignore(gitignore_content)
        
        parser = GitignoreParser(str(self.temp_path / '.gitignore'))
        
        # Create test files
        log_file = self.create_file("test.log")
        tmp_file = self.create_file("temp.tmp")
        py_file = self.create_file("script.py")
        
        self.assertTrue(parser.is_ignored(log_file))
        self.assertTrue(parser.is_ignored(tmp_file))
        self.assertFalse(parser.is_ignored(py_file))
    
    def test_directory_pattern(self):
        """Test directory pattern matching."""
        gitignore_content = "__pycache__/\nnode_modules/"
        self.create_gitignore(gitignore_content)
        
        parser = GitignoreParser(str(self.temp_path / '.gitignore'))
        
        # Create test files in directories
        pycache_file = self.create_file("__pycache__/test.pyc")
        node_file = self.create_file("node_modules/package.json")
        regular_file = self.create_file("src/main.py")
        
        self.assertTrue(parser.is_ignored(pycache_file))
        self.assertTrue(parser.is_ignored(node_file))
        self.assertFalse(parser.is_ignored(regular_file))
    
    def test_negation_pattern(self):
        """Test negation patterns with !."""
        gitignore_content = "*.log\n!important.log"
        self.create_gitignore(gitignore_content)
        
        parser = GitignoreParser(str(self.temp_path / '.gitignore'))
        
        # Create test files
        regular_log = self.create_file("debug.log")
        important_log = self.create_file("important.log")
        
        self.assertTrue(parser.is_ignored(regular_log))
        self.assertFalse(parser.is_ignored(important_log))
    
    def test_path_specific_pattern(self):
        """Test path-specific patterns."""
        gitignore_content = "src/*.tmp\n/build"
        self.create_gitignore(gitignore_content)
        
        parser = GitignoreParser(str(self.temp_path / '.gitignore'))
        
        # Create test files
        src_tmp = self.create_file("src/temp.tmp")
        other_tmp = self.create_file("other/temp.tmp")
        build_file = self.create_file("build/output.txt")
        
        self.assertTrue(parser.is_ignored(src_tmp))
        self.assertFalse(parser.is_ignored(other_tmp))
        self.assertTrue(parser.is_ignored(build_file))
    
    def test_comments_and_empty_lines(self):
        """Test that comments and empty lines are ignored."""
        gitignore_content = """
# This is a comment
*.log

# Another comment
*.tmp
        """
        self.create_gitignore(gitignore_content)
        
        parser = GitignoreParser(str(self.temp_path / '.gitignore'))
        
        log_file = self.create_file("test.log")
        tmp_file = self.create_file("test.tmp")
        
        self.assertTrue(parser.is_ignored(log_file))
        self.assertTrue(parser.is_ignored(tmp_file))
    
    def test_wildcard_patterns(self):
        """Test wildcard patterns."""
        gitignore_content = "test_*\n*.py[co]"
        self.create_gitignore(gitignore_content)
        
        parser = GitignoreParser(str(self.temp_path / '.gitignore'))
        
        test_file = self.create_file("test_something.txt")
        pyc_file = self.create_file("module.pyc")
        pyo_file = self.create_file("module.pyo")
        py_file = self.create_file("module.py")
        
        self.assertTrue(parser.is_ignored(test_file))
        self.assertTrue(parser.is_ignored(pyc_file))
        self.assertTrue(parser.is_ignored(pyo_file))
        self.assertFalse(parser.is_ignored(py_file))


class TestGitignoreUtilityFunctions(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_gitignore(self, content: str, path: Path | None = None):
        """Helper method to create a .gitignore file."""
        if path is None:
            path = self.temp_path
        gitignore_path = path / '.gitignore'
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(gitignore_path)
    
    def create_file(self, relative_path: str):
        """Helper method to create a file."""
        file_path = self.temp_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
        return str(file_path)
    
    def test_find_gitignore_files(self):
        """Test finding .gitignore files in directory hierarchy."""
        # Create nested directory structure
        subdir = self.temp_path / "subdir" / "nested"
        subdir.mkdir(parents=True)
        
        # Create .gitignore files at different levels
        root_gitignore = self.create_gitignore("*.log", self.temp_path)
        sub_gitignore = self.create_gitignore("*.tmp", self.temp_path / "subdir")
        
        # Test from nested directory
        gitignore_files = find_gitignore_files(str(subdir))
        
        self.assertIn(root_gitignore, gitignore_files)
        self.assertIn(sub_gitignore, gitignore_files)
    
    def test_should_ignore_file_git_directory(self):
        """Test that .git directory is always ignored."""
        git_file = self.create_file(".git/config")
        git_subfile = self.create_file(".git/objects/abc123")
        
        self.assertTrue(should_ignore_file(git_file, []))
        self.assertTrue(should_ignore_file(git_subfile, []))
    
    def test_should_ignore_file_with_gitignore(self):
        """Test file ignoring with .gitignore rules."""
        gitignore_content = "*.log\n__pycache__/"
        gitignore_path = self.create_gitignore(gitignore_content)
        
        log_file = self.create_file("debug.log")
        py_file = self.create_file("script.py")
        cache_file = self.create_file("__pycache__/module.pyc")
        
        gitignore_files = [gitignore_path]
        
        self.assertTrue(should_ignore_file(log_file, gitignore_files))
        self.assertFalse(should_ignore_file(py_file, gitignore_files))
        self.assertTrue(should_ignore_file(cache_file, gitignore_files))
    
    def test_filter_files_by_gitignore(self):
        """Test filtering a list of files by gitignore rules."""
        gitignore_content = "*.log\n*.tmp\n__pycache__/"
        self.create_gitignore(gitignore_content)
        
        # Create test files
        files = [
            self.create_file("script.py"),
            self.create_file("debug.log"),
            self.create_file("temp.tmp"),
            self.create_file("__pycache__/module.pyc"),
            self.create_file(".git/config"),
            self.create_file("README.md")
        ]
        
        filtered_files = filter_files_by_gitignore(files, str(self.temp_path))
        
        # Should only contain .py and .md files
        filtered_names = [Path(f).name for f in filtered_files]
        self.assertIn("script.py", filtered_names)
        self.assertIn("README.md", filtered_names)
        self.assertNotIn("debug.log", filtered_names)
        self.assertNotIn("temp.tmp", filtered_names)
        self.assertNotIn("module.pyc", filtered_names)
        self.assertNotIn("config", filtered_names)
    
    def test_filter_files_no_gitignore(self):
        """Test filtering when no .gitignore exists (should only exclude .git)."""
        files = [
            self.create_file("script.py"),
            self.create_file("debug.log"),
            self.create_file(".git/config"),
            self.create_file("README.md")
        ]
        
        filtered_files = filter_files_by_gitignore(files, str(self.temp_path))
        
        # Should exclude only .git files
        filtered_names = [Path(f).name for f in filtered_files]
        self.assertIn("script.py", filtered_names)
        self.assertIn("debug.log", filtered_names)
        self.assertIn("README.md", filtered_names)
        self.assertNotIn("config", filtered_names)
    
    def test_complex_gitignore_patterns(self):
        """Test complex gitignore patterns from real-world scenarios."""
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
config/local.py
!config/local.example.py
        """
        self.create_gitignore(gitignore_content)
        
        # Create test files
        files = [
            self.create_file("main.py"),
            self.create_file("__pycache__/main.cpython-39.pyc"),
            self.create_file("module.pyc"),
            self.create_file("build/lib/module.py"),
            self.create_file(".vscode/settings.json"),
            self.create_file(".DS_Store"),
            self.create_file("config/local.py"),
            self.create_file("config/local.example.py"),
            self.create_file("README.md")
        ]
        
        filtered_files = filter_files_by_gitignore(files, str(self.temp_path))
        filtered_names = [Path(f).name for f in filtered_files]
        
        # Should include
        self.assertIn("main.py", filtered_names)
        self.assertIn("local.example.py", filtered_names)
        self.assertIn("README.md", filtered_names)
        
        # Should exclude
        self.assertNotIn("main.cpython-39.pyc", filtered_names)
        self.assertNotIn("module.pyc", filtered_names)
        self.assertNotIn("settings.json", filtered_names)
        self.assertNotIn(".DS_Store", filtered_names)
        self.assertNotIn("local.py", filtered_names)


if __name__ == '__main__':
    unittest.main()
