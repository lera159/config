import unittest
from emulator import ShellEmulator
from io import BytesIO
import zipfile

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        """Set up a virtual file system for testing."""
        self.username = "test_user"
        self.virtual_fs_data = BytesIO()

        with zipfile.ZipFile(self.virtual_fs_data, mode='w') as zf:
            zf.writestr('virtual_fs/bin/script.sh', 'echo Hello World')
            zf.writestr('virtual_fs/home/', '')
            zf.writestr('virtual_fs/usr/', '')

        self.virtual_fs_data.seek(0)
        self.emulator = ShellEmulator(self.virtual_fs_data, self.username)

    def test_list_files_root(self):
        """Test listing files in the root directory."""
        self.emulator.current_path = "/"
        output = self._capture_output(self.emulator.list_files)
        self.assertIn("virtual_fs", output)

    def test_change_directory(self):
        """Test changing directories."""
        self.emulator.change_directory("virtual_fs")
        self.assertEqual(self.emulator.current_path, "/virtual_fs/")

    def test_list_files_virtual_fs(self):
        """Test listing files in /virtual_fs."""
        self.emulator.current_path = "/virtual_fs/"
        output = self._capture_output(self.emulator.list_files)
        self.assertIn("bin", output)
        self.assertIn("home", output)
        self.assertIn("usr", output)

    def test_move_file(self):
        """Test moving a file."""
        self.emulator.current_path = "/virtual_fs/bin/"
        self.emulator.move_file("script.sh", "../home/script.sh")
        
        self.emulator.current_path = "/virtual_fs/home/"
        output = self._capture_output(self.emulator.list_files)
        self.assertIn("Пустая директория", output)

    def test_command_execution(self):
        """Test execution of multiple commands."""
        self.emulator.execute_command("cd virtual_fs")
        self.assertEqual(self.emulator.current_path, "/virtual_fs/")

        self.emulator.execute_command("cd bin")
        self.assertEqual(self.emulator.current_path, "/virtual_fs/bin/")

        output = self._capture_output(lambda: self.emulator.execute_command("ls"))
        self.assertIn("script.sh", output)

    def _capture_output(self, func):
        """Helper method to capture printed output."""
        import sys
        from io import StringIO

        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            func()
            return sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

if __name__ == "__main__":
    unittest.main()
