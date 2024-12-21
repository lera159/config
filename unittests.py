import unittest
from unittest.mock import patch, mock_open
import subprocess
import xml.etree.ElementTree as ET
import os
from hw2 import read_config, get_commit_tree, generate_graphviz_code, write_output

class TestGitCommitGraph(unittest.TestCase):

    def test_read_config(self):
        # Test for successful reading of config file
        config_xml = """<config>
            <repo_path>/path/to/repo</repo_path>
            <output_path>/path/to/output</output_path>
        </config>"""
        with patch("builtins.open", mock_open(read_data=config_xml)):
            result = read_config("config.xml")
            self.assertEqual(result['repo_path'], "/path/to/repo")
            self.assertEqual(result['output_path'], "/path/to/output")

    @patch("subprocess.run")
    def test_get_commit_tree(self, mock_subprocess_run):
        # Test for successful commit tree extraction
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["git", "-C", "/path/to/repo", "log", "--pretty=format:%H %s", "--reverse"],
            returncode=0,
            stdout="abc123 Initial commit\nabc456 Added feature X\n",
            stderr=""
        )

        result = get_commit_tree("/path/to/repo")
        expected_result = {
            "abc123": {"message": "Initial commit", "children": []},
            "abc456": {"message": "Added feature X", "children": []}
        }

        self.assertEqual(result, expected_result)

    @patch("subprocess.run")
    def test_get_commit_tree_failure(self, mock_subprocess_run):
        # Test when subprocess fails to run
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["git", "-C", "/path/to/repo", "log", "--pretty=format:%H %s", "--reverse"],
            returncode=1,
            stdout="",
            stderr="error: failed to run git log"
        )

        result = get_commit_tree("/path/to/repo")
        self.assertEqual(result, {})

def test_generate_graphviz_code(self):
    # Test for generating correct Graphviz DOT code
    commit_info = {
        "abc123": {"message": "Initial commit", "children": []},
        "abc456": {"message": "Added feature X", "children": []}
    }

    expected_output = '''digraph G {
    node [shape=box, style=filled, fillcolor=lightyellow];
    "abc123" [label="Initial commit\\nabc123"];
    "abc123" -> "abc456";
    "abc456" [label="Added feature X\\nabc456"];
}'''

    result = generate_graphviz_code(commit_info)
    self.assertEqual(result.strip(), expected_output.strip())



    @patch("builtins.open", mock_open())
    def test_write_output(self):
        # Test that write_output correctly writes to a file
        output_content = "some content"
        write_output("output.dot", output_content)
        # Verify if open was called with the correct file path and content
        open.assert_called_with("output.dot", 'w')
        open().write.assert_called_with(output_content)

if __name__ == "__main__":
    unittest.main()
