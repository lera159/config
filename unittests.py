import unittest
from unittest.mock import mock_open, patch
import yaml

from hw3 import (
    parse_input_file,
    remove_comments,
    parse_dictionary,
    parse_variables,
    convert_to_yaml
)

class TestConfigToYaml(unittest.TestCase):

    def test_parse_input_file(self):
        mock_content = "test content"
        with patch("builtins.open", mock_open(read_data=mock_content)) as mock_file:
            result = parse_input_file("dummy_path")
            mock_file.assert_called_once_with("dummy_path", 'r', encoding='utf-8')
            self.assertEqual(result, mock_content)

    def test_remove_comments(self):
        text_with_comments = (
            "person = table([name = \"John\", age = \"30\"])\n" 
            "* This is a comment\n"
            "{# multi-line\ncomment #}"
        )
        expected_result = "person = table([name = \"John\", age = \"30\"])"
        self.assertEqual(remove_comments(text_with_comments), expected_result)

    def test_parse_dictionary(self):
        text = "person = table([name = \"John\", age = \"30\"])"
        expected_result = {
            "person": {
                "name": "John",
                "age": "30"
            }
        }
        self.assertEqual(parse_dictionary(text), expected_result)

    def test_parse_dictionary_invalid_syntax(self):
        text = "person = table([name: \"John\", age = \"30\"])"
        with self.assertRaises(ValueError) as context:
            parse_dictionary(text)
        self.assertIn("Синтаксическая ошибка", str(context.exception))

    def test_parse_variables(self):
        text = (
            "person = table([name = \"John\", age = \"30\"])\n"
            "greeting = \"Hello\"\n"
        )
        parsed_data = {
            "person": {
                "name": "John",
                "age": "30"
            }
        }
        expected_variables = {
            "greeting": "Hello"
        }
        self.assertEqual(parse_variables(text, parsed_data), expected_variables)

    def test_parse_variables_with_existing_key(self):
        text = (
            "person = table([name = \"John\", age = \"30\"])\n"
            "name = \"John\"\n"
        )
        parsed_data = {
            "person": {
                "name": "John",
                "age": "30"
            }
        }
        expected_variables = {}
        self.assertEqual(parse_variables(text, parsed_data), expected_variables)

    def test_convert_to_yaml(self):
        data = {
            "person": {
                "name": "John",
                "age": "30"
            },
            "greeting": "Hello"
        }
        yaml_output = convert_to_yaml(data)
        parsed_yaml = yaml.safe_load(yaml_output)
        self.assertEqual(parsed_yaml, data)

if __name__ == "__main__":
    unittest.main()
