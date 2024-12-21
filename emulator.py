import os
import zipfile
import sys
import argparse
import shutil

class ShellEmulator:
    def __init__(self, virtual_fs_path, username):
        self.current_path = "/"
        self.history = []
        self.username = username
        self.virtual_fs_path = virtual_fs_path
        self.virtual_fs = None

        self.extract_virtual_fs()

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Запуск эмулятора командной строки vshell.')
        parser.add_argument('--username', type=str, required=True, help='Имя пользователя для показа в приглашении к вводу.')
        parser.add_argument('virtual_fs', type=str, help='Путь к архиву виртуальной файловой системы (zip).')
        
        args = parser.parse_args()
        
        if not os.path.exists(args.virtual_fs):
            parser.error(f"Файл виртуальной файловой системы '{args.virtual_fs}' не найден.")
        
        return args

    def extract_virtual_fs(self):
        """Extract the virtual file system from the zip archive."""
        if not os.path.exists(self.virtual_fs_path):
            print("Ошибка: Файл виртуальной файловой системы не найден.")
            sys.exit(1)

        # Open the zip archive and create a directory for the virtual file system
        self.virtual_fs = zipfile.ZipFile(self.virtual_fs_path, 'r')
        self.virtual_fs.extractall("virtual_fs")

    def list_files(self):
        """Simulate the 'ls' command."""
        path = f"virtual_fs{self.current_path}"
        try:
            files = os.listdir(path)
            if files:
                print("\n".join(files))
            else:
                print("Пустая директория")
        except FileNotFoundError:
            print("Директория не найдена")

    def change_directory(self, path):
        """Simulate the 'cd' command."""
        if path == "..":
            if self.current_path != "/":
                self.current_path = os.path.dirname(self.current_path) or "/"
            else:
                print("Вы находитесь в корневой директории.")
        else:
            new_path = os.path.join(f"virtual_fs{self.current_path}", path)
            if os.path.isdir(new_path):
                self.current_path = os.path.join(self.current_path, path)
            else:
                print("Директория не найдена.")

    def print_working_directory(self):
        """Simulate the 'pwd' command."""
        print(f"{self.username}:{self.current_path}")

    def move_file(self, source, destination):
        """Simulate the 'mv' command."""
        src_path = os.path.join(f"virtual_fs{self.current_path}", source)
        dst_path = os.path.join(f"virtual_fs{self.current_path}", destination)

        if not os.path.exists(src_path):
            print("Файл или директория для перемещения не найдены.")
            return
        
        try:
            shutil.move(src_path, dst_path)
            print(f"Файл/директория '{source}' перемещен(а) в '{destination}'.")
        except Exception as e:
            print(f"Ошибка при перемещении: {str(e)}")

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
