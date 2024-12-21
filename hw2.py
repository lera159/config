import subprocess
import xml.etree.ElementTree as ET
import os

def read_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()
    config = {
        'repo_path': root.find('repo_path').text,
        'output_path': root.find('output_path').text
    }
    return config

def get_commit_tree(repo_path):
    result = subprocess.run(
        ['git', '-C', repo_path, 'log', '--pretty=format:%H %s', '--reverse'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8' 
    )
    
    if result.returncode != 0:
        print("Ошибка при получении коммитов:", result.stderr)
        return {}

    commits = result.stdout.splitlines()
    commit_info = {}  # информация для каждого коммита
    
    for commit in commits:
        hash_value, message = commit.split(' ', 1)
        commit_info[hash_value] = {
            'message': message,
            'children': []
        }

    return commit_info

def generate_graphviz_code(commit_info):
    lines = ["digraph G {", "    node [shape=box, style=filled, fillcolor=lightyellow];"]
    
    previous_commit = None
    
    for commit_hash, info in commit_info.items():
        short_commit_hash = commit_hash[:7]  # showing short commit hash
        commit_node = f'    "{short_commit_hash}" [label="{info["message"]}\\n{commit_hash}"];'
        lines.append(commit_node)

        if previous_commit:
            lines.append(f'    "{previous_commit}" -> "{short_commit_hash}";')

        previous_commit = short_commit_hash

    lines.append("}")  
    
    return "\n".join(lines)



def write_output(output_path, content):
    with open(output_path, 'w') as f:
        f.write(content)

def main(config_path):
    config = read_config(config_path)
    commit_info = get_commit_tree(config['repo_path'])
    graphviz_code = generate_graphviz_code(commit_info)
    print(graphviz_code)
    write_output(config['output_path'], graphviz_code)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.argv.append("config.xml")
    main(sys.argv[1])
