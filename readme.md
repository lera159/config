# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей при запуске

```
pip install subprocess

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
config.xml             # конфигурационный файл 
hw2.py                  # файл с программой
file.dot             # файл с выводом программы 
```

# 4. Запуск проекта
```bash
py hw2.py config.xml     # py название файла <файл с конфигом>
```


# 5. Тестирование с моим репозитеорием 
Вывод программы
```
digraph G {
    node [shape=box, style=filled, fillcolor=lightyellow];
    "585071c" [label="Initial commit\n585071c6722ad518536abab03d4b895b8db85858"];
    "1aa374f" [label="commit1\n1aa374feec842e0f8eeb3ea7e7eea0f8e3ef3510"];
    "585071c" -> "1aa374f";
    "8c0798c" [label="commit2\n8c0798ce186123f77f1c75a554f3033502525892"];
    "1aa374f" -> "8c0798c";
    "a74e491" [label="commit3\na74e4918d8e835bc978e15934f8bcee4ffa472bd"];
    "8c0798c" -> "a74e491";
    "2783202" [label="commit4\n2783202a60b365aa940563b7e5742d9e45f696c7"];
    "a74e491" -> "2783202";
}
```


