import os
import zipfile
import sys
import argparse
from io import BytesIO

class ShellEmulator:
    def __init__(self, virtual_fs_path, username):
        self.current_path = "/"
        self.history = []
        self.username = username
        self.virtual_fs_path = virtual_fs_path
        self.virtual_fs = None
        self.in_memory_fs = {}

        self.load_virtual_fs()

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Запуск эмулятора командной строки vshell.')
        parser.add_argument('--username', type=str, required=True, help='Имя пользователя для показа в приглашении к вводу.')
        parser.add_argument('virtual_fs', type=str, help='Путь к архиву виртуальной файловой системы (zip).')

        args = parser.parse_args()

        if not os.path.exists(args.virtual_fs):
            parser.error(f"Файл виртуальной файловой системы '{args.virtual_fs}' не найден.")

        return args

    def load_virtual_fs(self):
        """Load the virtual file system into memory."""
        if isinstance(self.virtual_fs_path, BytesIO):
            self.virtual_fs_path.seek(0)  # Убедитесь, что указатель в начале файла
            self.virtual_fs = zipfile.ZipFile(self.virtual_fs_path)
        elif os.path.exists(self.virtual_fs_path):
            with open(self.virtual_fs_path, 'rb') as file:
                self.virtual_fs = zipfile.ZipFile(BytesIO(file.read()))
        else:
            print("Ошибка: Файл виртуальной файловой системы не найден.")
            sys.exit(1)

        for name in self.virtual_fs.namelist():
            self.in_memory_fs[name] = self.virtual_fs.read(name)


    def list_files(self):
        """Simulate the 'ls' command."""
        try:
            files = [
                name[len(self.current_path.lstrip('/')):].split('/')[0]
                for name in self.in_memory_fs.keys()
                if name.startswith(self.current_path.lstrip('/')) and name != self.current_path.lstrip('/')
            ]
            files = sorted(set(files))
            print("\n".join(files) if files else "Пустая директория")
        except Exception as e:
            print(f"Ошибка при перечислении файлов: {str(e)}")

    def change_directory(self, path):
        """Simulate the 'cd' command."""
        if path == "..":
            if self.current_path != "/":
                self.current_path = os.path.dirname(self.current_path.rstrip('/')) or "/"
            else:
                print("Вы находитесь в корневой директории.")
        else:
            new_path = os.path.join(self.current_path, path).rstrip('/') + '/'
            if any(name.startswith(new_path.lstrip('/')) for name in self.in_memory_fs.keys()):
                self.current_path = new_path
            else:
                print("Директория не найдена.")

    def print_working_directory(self):
        """Simulate the 'pwd' command."""
        print(f"{self.username}:{self.current_path}")

    def move_file(self, source, destination):
        """Simulate the 'mv' command."""
        source_path = os.path.join(self.current_path.lstrip('/'), source).lstrip('/')
        destination_path = os.path.join(self.current_path.lstrip('/'), destination).lstrip('/')

        if source_path not in self.in_memory_fs:
            print("Файл или директория для перемещения не найдены.")
            return

        if destination_path in self.in_memory_fs:
            print("Ошибка: Целевой файл уже существует.")
            return

        # Perform the move operation in memory
        self.in_memory_fs[destination_path] = self.in_memory_fs.pop(source_path)
        print(f"Файл/директория '{source}' перемещен(а) в '{destination}'.")

    def exit_shell(self):
        """Exit the shell emulator."""
        print("Выход из эмулятора.")
        sys.exit(0)

    def execute_command(self, command):
        """Parse and execute commands."""
        self.history.append(command)

        command_dict = {
            "ls": self.list_files,
            "cd": lambda path: self.change_directory(path),
            "pwd": self.print_working_directory,
            "mv": lambda src, dst: self.move_file(src, dst),
            "exit": self.exit_shell,
            "history": self.show_history
        }

        parts = command.split()
        cmd_func = command_dict.get(parts[0])

        if cmd_func:
            if parts[0] == "cd":
                cmd_func(parts[1]) if len(parts) > 1 else print("Нужен аргумент для команды cd.")
            elif parts[0] == "mv":
                if len(parts) > 2:
                    cmd_func(parts[1], parts[2])
                else:
                    print("Нужны два аргумента для команды mv.")
            else:
                cmd_func()
        else:
            print(f"{self.username}: команда не найдена")

    def show_history(self):
        """Show the command history."""
        if self.history:
            print("\n".join(self.history))
        else:
            print("История пуста.")

if __name__ == "__main__":
    args = ShellEmulator.parse_arguments()
    emulator = ShellEmulator(args.virtual_fs, args.username)

    while True:
        try:
            command = input(f"{args.username}:{emulator.current_path} $ ")
            emulator.execute_command(command.strip())
        except EOFError:
            emulator.exit_shell()
