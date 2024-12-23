import os
import zlib
import xml.etree.ElementTree as ET

def read_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()
    config = {
        'repo_path': root.find('repo_path').text,
        'output_path': root.find('output_path').text,
        'branch_name': root.find('branch_name').text
    }
    return config

def read_object(repo_path, sha):
    object_path = os.path.join(repo_path, '.git', 'objects', sha[:2], sha[2:])
    with open(object_path, 'rb') as f:
        compressed_data = f.read()
    decompressed_data = zlib.decompress(compressed_data)
    return decompressed_data

def get_ref_commit(repo_path, branch_name):
    ref_path = os.path.join(repo_path, '.git', 'refs', 'heads', branch_name)
    if not os.path.exists(ref_path):
        raise ValueError(f"Branch '{branch_name}' does not exist.")
    with open(ref_path, 'r') as f:
        return f.read().strip()

def parse_commit(commit_data):
    lines = commit_data.splitlines()
    tree = None
    parents = []
    message_start = False
    message = ""

    for line in lines:
        if line.startswith(b'tree '):
            tree = line.split(b' ')[1].decode()
        elif line.startswith(b'parent '):
            parents.append(line.split(b' ')[1].decode())
        elif line == b'':
            message_start = True  
        elif message_start:  
            message += line.decode() + '\n'

    return tree, parents, message.strip()


def parse_tree(repo_path, tree_sha):
    tree_data = read_object(repo_path, tree_sha)
    files = []
    i = 0
    while i < len(tree_data):
        space_idx = tree_data.find(b' ', i)
        null_idx = tree_data.find(b'\x00', space_idx)
        file_mode = tree_data[i:space_idx].decode()
        file_name = tree_data[space_idx + 1:null_idx].decode()
        file_sha = tree_data[null_idx + 1:null_idx + 21].hex()
        files.append(file_name)
        i = null_idx + 21
    return files

def get_commit_tree(repo_path, branch_name):
    commit_info = {}
    
    start_commit = get_ref_commit(repo_path, branch_name)
    stack = [start_commit]
    
    while stack:
        current_commit = stack.pop()
        if current_commit in commit_info:
            continue

        commit_data = read_object(repo_path, current_commit)
        tree, parents, message = parse_commit(commit_data)
        files = parse_tree(repo_path, tree) if tree else []

        commit_info[current_commit] = {
            'message': message,
            'files': files,
            'children': []
        }

        for parent in parents:
            commit_info[current_commit]['children'].append(parent)
            stack.append(parent)

    return commit_info

def generate_graphviz_code(commit_info):
    lines = ["digraph G {", "    node [shape=box, style=filled, fillcolor=lightyellow];"]

    for commit_hash, info in commit_info.items():
        short_commit_hash = commit_hash[:7]  # showing short commit hash
        # Use only the first line of the commit message as the name
        commit_name = info["message"].splitlines()[0] if info["message"] else "No Message"
        files_list = "\\n".join(info['files'])
        commit_node = f'    "{short_commit_hash}" [label="{commit_name}\\n{commit_hash}\\n{files_list}"];'
        lines.append(commit_node)

        for child in info['children']:
            lines.append(f'    "{child[:7]}" -> "{short_commit_hash}";')

    lines.append("}")

    return "\n".join(lines)


def write_output(output_path, content):
    with open(output_path, 'w') as f:
        f.write(content)

def main(config_path):
    config = read_config(config_path)
    commit_info = get_commit_tree(config['repo_path'], config['branch_name'])
    graphviz_code = generate_graphviz_code(commit_info)
    print(graphviz_code)
    write_output(config['output_path'], graphviz_code)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.argv.append("config.xml")
    main(sys.argv[1])
