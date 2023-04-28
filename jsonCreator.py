import os
import re
import json

def get_file_contents(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def get_references(text):
    return re.findall('\[\[(.*?)\]\]', text)

def extract_title(contents):
    title_match = re.search('# (.+)', contents)
    if title_match:
        return title_match.group(1)
    else:
        return "ERROR"

def parse_file(filepath):
    filename = os.path.basename(filepath)
    contents = get_file_contents(filepath)
    references = get_references(contents)
    title = extract_title(contents)
    return {
        'id': title,
        'filename': filename,
        'text': contents,
        'references': references
    }

def get_node_id(node):
    return node['id']

def create_links(nodes, node_ids):
    links = []
    for node in nodes:
        for reference in node['references']:
            if reference in node_ids:
                links.append({
                    'source': node['id'],
                    'target': reference
                })
    return links

def create_graph(filepaths):
    nodes = [parse_file(f) for f in filepaths]
    node_ids = [get_node_id(n) for n in nodes]
    links = create_links(nodes, node_ids)
    return {
        'nodes': nodes,
        'links': links
    }


filepaths = ['note1.md', 'note2.md', 'note3.md']
graph = create_graph(filepaths)

with open("my_json_file.json", "w") as f:
    json.dump(graph, f)
