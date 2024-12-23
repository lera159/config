# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей при запуске

```
pip install tkinter
pip install zipfile
pip install argparse
pip install shutil

```

# Создайте виртуальное окружение

```bash
# Активируйте виртуальное окружение
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для MacOS/Linux:
source venv/bin/activate
```


# 3. Структура проекта
Проект содержит следующие файлы и директории:
```bash
unittests.py              # файл для тестирования
virtual_fs.zip           # tar-архив в качестве образа файловой системы
emulator.py                  # файл с программой
```

# 4. Запуск проекта
```bash
py emulator.py <username> virtual_fs.zip     # py название файла <файл с образом файловой системы>
```

# 5. Команды 
```bash
ls
cd <dir>
mv <from> <to>    #mv /home/test.txt /bin/
history
exit
```
