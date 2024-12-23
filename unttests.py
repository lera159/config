import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import tkinter as tk
from emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.emulator = ShellEmulator(self.root, "virtual_fs.tar")

    @patch('os.listdir', return_value=['file1.txt', 'file2.txt'])
    def test_list_files(self, mock_listdir):
        self.emulator.list_files()
        self.assertIn("file1.txt", self.emulator.text_area.get("1.0", tk.END))
        self.assertIn("file2.txt", self.emulator.text_area.get("1.0", tk.END))

    @patch('os.path.isdir', return_value=True)
    def test_change_directory(self, mock_isdir):
        self.emulator.change_directory("subdir")
        self.assertEqual(self.emulator.current_path, "/subdir")

    @patch('os.path.isdir', return_value=False)
    def test_change_directory_not_found(self, mock_isdir):
        self.emulator.change_directory("nonexistent")
        self.assertIn("Директория не найдена", self.emulator.text_area.get("1.0", tk.END))

    def test_print_working_directory(self):
        self.emulator.print_working_directory()
        self.assertIn(f"{self.emulator.username}:/", self.emulator.text_area.get("1.0", tk.END))

    @patch('builtins.open', new_callable=mock_open, read_data="file content")
    def test_cat_file(self, mock_file):
        self.emulator.cat_file("file1.txt")
        self.assertIn("file content", self.emulator.text_area.get("1.0", tk.END))

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_cat_file_not_found(self, mock_file):
        self.emulator.cat_file("nonexistent.txt")
        self.assertIn("Файл не найден", self.emulator.text_area.get("1.0", tk.END))

    @patch('builtins.open', new_callable=mock_open)
    def test_touch_file(self, mock_file):
        self.emulator.touch_file("newfile.txt")
        self.assertIn("Файл 'newfile.txt' создан.", self.emulator.text_area.get("1.0", tk.END))

    def test_show_history(self):
        self.emulator.history = ["ls", "pwd", "cd subdir"]
        self.emulator.show_history()
        self.assertIn("ls\npwd\ncd subdir", self.emulator.text_area.get("1.0", tk.END))

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()