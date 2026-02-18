import unittest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from clipcode.cli import main


class TestCLI(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_file(self, relative_path: str, content: str = "test content"):
        """Helper method to create a file in the temp directory."""
        file_path = self.temp_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(file_path)
    
    def create_gitignore(self, content: str):
        """Helper method to create a .gitignore file."""
        gitignore_path = self.temp_path / '.gitignore'
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(gitignore_path)
    
    @patch('clipcode.cli.export_files_to_clipboard')
    def test_cli_basic_usage(self, mock_export):
        """Test basic CLI usage without extensions."""
        test_args = ['clipcode', str(self.temp_path)]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        # Verify export_files_to_clipboard was called with correct arguments
        mock_export.assert_called_once_with(str(self.temp_path), None, True, [], 3000, 500)
    
    @patch('clipcode.cli.export_files_to_clipboard')
    def test_cli_with_extensions(self, mock_export):
        """Test CLI usage with file extensions."""
        test_args = ['clipcode', str(self.temp_path), 'py', 'js', 'ts']
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        # Verify export_files_to_clipboard was called with extensions
        mock_export.assert_called_once_with(str(self.temp_path), ['py', 'js', 'ts'], True, [], 3000, 500)
    
    @patch('clipcode.cli.export_files_to_clipboard')
    def test_cli_respect_gitignore_default(self, mock_export):
        """Test that --respect-gitignore is the default behavior."""
        test_args = ['clipcode', str(self.temp_path)]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        # Third argument should be True (respect_gitignore=True)
        mock_export.assert_called_once_with(str(self.temp_path), None, True, [], 3000, 500)
    
    @patch('clipcode.cli.export_files_to_clipboard')
    def test_cli_explicit_respect_gitignore(self, mock_export):
        """Test explicit --respect-gitignore flag."""
        test_args = ['clipcode', '--respect-gitignore', str(self.temp_path)]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        mock_export.assert_called_once_with(str(self.temp_path), None, True, [], 3000, 500)
    
    @patch('clipcode.cli.export_files_to_clipboard')
    def test_cli_no_respect_gitignore(self, mock_export):
        """Test --no-respect-gitignore flag."""
        test_args = ['clipcode', '--no-respect-gitignore', str(self.temp_path)]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        # Third argument should be False (respect_gitignore=False)
        mock_export.assert_called_once_with(str(self.temp_path), None, False, [], 3000, 500)
    
    @patch('clipcode.cli.export_files_to_clipboard')
    def test_cli_complex_combination(self, mock_export):
        """Test CLI with extensions and gitignore options."""
        test_args = ['clipcode', '--no-respect-gitignore', str(self.temp_path), 'py', 'md']
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        mock_export.assert_called_once_with(str(self.temp_path), ['py', 'md'], False, [], 3000, 500)
    
    def test_cli_help_message(self):
        """Test that help message includes gitignore options."""
        test_args = ['clipcode', '--help']
        
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit):
                with patch('sys.stdout') as mock_stdout:
                    main()
        
        # Check that help was called (SystemExit with code 0)
        # This test mainly ensures the argument parser is set up correctly


    @patch('clipcode.cli.export_files_to_clipboard')
    def test_cli_with_ignore_patterns(self, mock_export):
        """Test CLI with explicit ignore patterns."""
        test_args = ['clipcode', '-i', 'foo.py,bar/baz.txt', '-i', '*.log', str(self.temp_path)]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        mock_export.assert_called_once_with(
            str(self.temp_path), None, True, ['foo.py', 'bar/baz.txt', '*.log'], 3000, 500
        )

    @patch('clipcode.cli.export_files_to_clipboard')
    def test_cli_with_truncate_lines_custom(self, mock_export):
        """Test CLI with custom --truncate-lines values."""
        test_args = ['clipcode', '--truncate-lines', '1200:300', str(self.temp_path)]

        with patch.object(sys, 'argv', test_args):
            main()

        mock_export.assert_called_once_with(str(self.temp_path), None, True, [], 1200, 300)

    @patch('clipcode.cli.export_files_to_clipboard')
    def test_cli_with_truncate_lines_ignore_mode(self, mock_export):
        """Test CLI where truncate target is 0 (ignore large files)."""
        test_args = ['clipcode', '--truncate-lines', '3000:0', str(self.temp_path)]

        with patch.object(sys, 'argv', test_args):
            main()

        mock_export.assert_called_once_with(str(self.temp_path), None, True, [], 3000, 0)

    def test_cli_with_truncate_lines_invalid_format(self):
        """Invalid --truncate-lines format should fail fast."""
        test_args = ['clipcode', '--truncate-lines', '3000', str(self.temp_path)]

        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit):
                main()

    def test_cli_with_truncate_lines_invalid_relation(self):
        """truncate_to must not be greater than truncate_from."""
        test_args = ['clipcode', '--truncate-lines', '100:200', str(self.temp_path)]

        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit):
                main()


class TestCLIIntegration(unittest.TestCase):
    """Integration tests for CLI functionality."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_file(self, relative_path: str, content: str = "test content"):
        """Helper method to create a file in the temp directory."""
        file_path = self.temp_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(file_path)
    
    def create_gitignore(self, content: str):
        """Helper method to create a .gitignore file."""
        gitignore_path = self.temp_path / '.gitignore'
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(gitignore_path)
    
    @patch('subprocess.run')
    def test_integration_with_gitignore(self, mock_subprocess):
        """Test full integration with gitignore filtering."""
        # Create test files
        self.create_file("main.py", "print('hello')")
        self.create_file("debug.log", "debug info")
        self.create_file("__pycache__/main.cpython-39.pyc", "compiled")
        self.create_file(".git/config", "git config")
        
        # Create .gitignore
        self.create_gitignore("*.log\n__pycache__/")
        
        # Mock subprocess.run to capture clipboard content
        mock_subprocess.return_value = MagicMock()
        
        test_args = ['clipcode', str(self.temp_path)]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        # Verify subprocess.run was called (clipboard operation)
        mock_subprocess.assert_called_once()
        
        # Get the content that would be copied to clipboard
        call_args = mock_subprocess.call_args
        clipboard_content = call_args[1]['input'].decode('utf-8')
        
        # Verify content includes main.py but excludes ignored files
        self.assertIn("main.py", clipboard_content)
        self.assertIn("print('hello')", clipboard_content)
        self.assertNotIn("debug.log", clipboard_content)
        self.assertNotIn("__pycache__", clipboard_content)
        self.assertNotIn(".git", clipboard_content)
    
    @patch('subprocess.run')
    def test_integration_without_gitignore(self, mock_subprocess):
        """Test integration when ignoring gitignore files."""
        # Create test files
        self.create_file("main.py", "print('hello')")
        self.create_file("debug.log", "debug info")
        self.create_file("__pycache__/main.cpython-39.pyc", "compiled")
        self.create_file(".git/config", "git config")
        
        # Create .gitignore (should be ignored)
        self.create_gitignore("*.log\n__pycache__/")
        
        # Mock subprocess.run
        mock_subprocess.return_value = MagicMock()
        
        test_args = ['clipcode', '--no-respect-gitignore', str(self.temp_path)]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        # Get clipboard content
        call_args = mock_subprocess.call_args
        clipboard_content = call_args[1]['input'].decode('utf-8')
        
        # Verify content includes files that would normally be ignored
        # (except .git which is always excluded)
        self.assertIn("main.py", clipboard_content)
        self.assertIn("debug.log", clipboard_content)
        self.assertIn("__pycache__", clipboard_content)
        self.assertNotIn(".git", clipboard_content)  # .git always excluded
    
    @patch('subprocess.run')
    def test_integration_with_extensions_and_gitignore(self, mock_subprocess):
        """Test integration with both extension filtering and gitignore."""
        # Create test files
        self.create_file("main.py", "print('hello')")
        self.create_file("script.js", "console.log('hello')")
        self.create_file("README.md", "# README")
        self.create_file("debug.log", "debug info")
        self.create_file("test.py", "test code")
        
        # Create .gitignore
        self.create_gitignore("*.log\ntest.py")
        
        # Mock subprocess.run
        mock_subprocess.return_value = MagicMock()
        
        test_args = ['clipcode', str(self.temp_path), 'py', 'js']
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        # Get clipboard content
        call_args = mock_subprocess.call_args
        clipboard_content = call_args[1]['input'].decode('utf-8')
        
        # Should include main.py and script.js
        self.assertIn("main.py", clipboard_content)
        self.assertIn("script.js", clipboard_content)
        
        # Should exclude README.md (wrong extension), debug.log and test.py (gitignored)
        self.assertNotIn("README.md", clipboard_content)
        self.assertNotIn("debug.log", clipboard_content)
        self.assertNotIn("test.py", clipboard_content)


if __name__ == '__main__':
    unittest.main()
