import argparse
import re
import sys
import yaml

def parse_input_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def remove_comments(text):
    # Удаляем однострочные комментарии
    text = re.sub(r'\*.*', '', text)
    # Удаляем многострочные комментарии
    text = re.sub(r'\{#.*?#\}', '', text, flags=re.DOTALL)
    return text.strip()

def parse_dictionary(text):
    dict_pattern = r'(\w+)\s*=\s*table\(\[(.*?)\]\)'
    matches = re.findall(dict_pattern, text, re.DOTALL)
    
    if not matches:
        raise ValueError("Синтаксическая ошибка: не найден словарь")

    result_dict = {}
    
    for match in matches:
        key = match[0].strip()
        items = match[1].strip().split(',')
        inner_dict = {}
        
        for item in items:
            item = item.strip()
            if '=' in item:
                k, v = item.split('=', 1)
                k = k.strip()
                v = v.strip().strip('"')
                inner_dict[k] = v
            else:
                raise ValueError(f"Синтаксическая ошибка: неверный элемент '{item}' в словаре")

        result_dict[key] = inner_dict

    return result_dict

def parse_variables(text, parsed_data):
    var_pattern = r'(\w+)\s*=\s*"([^"]+)"'
    matches = re.findall(var_pattern, text)
    
    variables = {}
    
    for match in matches:
        key, value = match
        key = key.strip()
        value = value.strip()
        
        # Проверяем наличие ключа и значения в parsed_data
        exists = False
        for k, v in parsed_data.items():
            if isinstance(v, dict) and k == 'person' and v.get(key) == value:
                exists = True
                break
        
        # Добавляем переменную только если её нет в parsed_data
        if not exists:
            variables[key] = value

    return variables

def convert_to_yaml(data):
    return yaml.dump(data, allow_unicode=True)

def main():
    parser = argparse.ArgumentParser(description='Преобразователь конфигурационного языка в YAML.')
    parser.add_argument('input_file', help='Путь к входному файлу с конфигурацией')
    
    args = parser.parse_args()
    
    try:
        input_text = parse_input_file(args.input_file)
        cleaned_text = remove_comments(input_text)
        
        parsed_data = parse_dictionary(cleaned_text)
        parsed_variables = parse_variables(cleaned_text, parsed_data)
        
        # Объединяем данные из словаря и переменных
        combined_data = {**parsed_data, **parsed_variables}

        yaml_output = convert_to_yaml(combined_data)
        
        print(yaml_output)
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()