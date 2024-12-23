import unittest
from unittest.mock import patch, mock_open
import zlib
from hw2 import *
# Mock data for testing
MOCK_COMMIT_DATA = b"""tree abcdef1234567890
parent 1234567890abcdef

Initial commit
"""
MOCK_TREE_DATA = b"100644 file.txt\x00" + bytes.fromhex("1234567890abcdef1234567890abcdef12345678")
MOCK_REPO_PATH = "/mock/repo"
MOCK_CONFIG_XML = """<config><repo_path>/mock/repo</repo_path><output_path>/mock/output.dot</output_path><branch_name>main</branch_name></config>"""

class TestGitGraphGenerator(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="abcdef1234567890")
    @patch("os.path.exists", return_value=True)
    def test_get_ref_commit(self, mock_exists, mock_open_file):
        branch_name = "main"
        ref = get_ref_commit(MOCK_REPO_PATH, branch_name)
        self.assertEqual(ref, MOCK_COMMIT_DATA.decode().splitlines()[0].split()[1])

    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_TREE_DATA)
    @patch("zlib.decompress", return_value=MOCK_TREE_DATA)
    def test_parse_tree(self, mock_decompress, mock_open_file):

        files = parse_tree(MOCK_REPO_PATH, "abcdef1234567890")
        self.assertEqual(files, ["file.txt"])

    @patch("zlib.decompress", return_value=MOCK_COMMIT_DATA)
    def test_parse_commit(self, mock_decompress):

        tree, parents, message = parse_commit(MOCK_COMMIT_DATA)
        self.assertEqual(tree, "abcdef1234567890")
        self.assertEqual(parents, ["1234567890abcdef"])
        self.assertEqual(message, "Initial commit")

    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_CONFIG_XML)
    def test_read_config(self, mock_open_file):

        config = read_config("/mock/config.xml")
        self.assertEqual(config["repo_path"], "/mock/repo")
        self.assertEqual(config["output_path"], "/mock/output.dot")
        self.assertEqual(config["branch_name"], "main")

    def test_generate_graphviz_code(self):
        commit_info = {
            "abcdef1": {
                "message": "Initial commit",
                "files": ["file.txt"],
                "children": ["1234567"]
            },
            "1234567": {
                "message": "Parent commit",
                "files": ["readme.md"],
                "children": []
            }
        }
        graphviz_code = generate_graphviz_code(commit_info)
        self.assertIn("digraph G {", graphviz_code)
        self.assertIn("abcdef1", graphviz_code)
        self.assertIn("1234567", graphviz_code)
        self.assertIn("file.txt", graphviz_code)
        self.assertIn("readme.md", graphviz_code)

if __name__ == "__main__":
    unittest.main()
