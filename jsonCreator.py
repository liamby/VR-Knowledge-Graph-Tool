import os
import re
import json
import glob

def shorten_text(text):
    words = text.split()[:15]
    if len(words) < len(text.split()):
        words.append('...')
    return ' '.join(words)

def remove_md_extension(filename):
    return os.path.splitext(filename)[0]

def get_file_contents(filepath):
    with open(filepath, encoding='utf-8') as f:
        return f.read()

def get_references(text):
    return re.findall('\[\[(.*?)\]\]', text)

def extract_title(contents, fileNameNoExtension):
    title_match = re.search('# (.+)', contents)
    if title_match:
        return title_match.group(1)
    else:
        return fileNameNoExtension

def extract_text(contents, fileNameNoExtension):
    title_match = re.search('# (.+)', contents)
    if title_match:
        start_index = title_match.end() + 1
        end_index = contents.find('[[', start_index)
        if end_index == -1:
            end_index = len(contents)
        return contents[start_index:end_index].strip()
    else:
        return fileNameNoExtension

def parse_file(filepath):
    filename = os.path.basename(filepath)
    rawContents = get_file_contents(filepath)
    references = get_references(rawContents)
    fileNameNoExtension = remove_md_extension(filename)
    text = extract_text(rawContents, fileNameNoExtension)
    shortenedText = shorten_text(text)
    title = extract_title(rawContents, fileNameNoExtension)
    return {
        'id': title,
        'filename': filename,
        'text': text,
        'references': references,
        'shortenedText': shortenedText,
        'rawContents': rawContents
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


md_files = []
for root, directories, files in os.walk('./myMarkdownFiles'):
    for file in files:
        if file.endswith('.md'):
            md_files.append(os.path.join(root, file))

graph = create_graph(md_files)

with open("my_json_file.json", "w") as f:
    json.dump(graph, f)
    