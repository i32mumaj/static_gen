import re
import os

from block import BlockType, markdown_to_html_node

def extract_title(markdown: str) -> str:
    line = re.search(r'^#\s.*$', markdown, re.MULTILINE)
    if line:
        return line.group().lstrip('#').strip()
    raise Exception("No title found in the markdown content.")


def generate_page(from_path: str, template_path: str, to_path: str) -> None:
    print(f"Generating page from {from_path} using template {template_path} to {to_path}")
    with open(from_path, 'r') as f:
        markdown_content = f.read()
  
    with open(template_path, 'r') as f:
        template_content = f.read()

    htmlstring = markdown_to_html_node(markdown_content) 
    htmlstring = htmlstring.to_html()

    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", htmlstring)

    with open(to_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursively(from_dir: str, template_path: str, to_dir: str) -> None:
    print(f"Generating pages recursively from {from_dir} to {to_dir} using template {template_path}")
    print(f"{os.listdir(from_dir)}")
    for file in os.listdir(from_dir):
        print(f"Found file: {file}")
        from_path = os.path.join(from_dir, file)
        print(f"Processing {from_path}")
        if os.path.isdir(from_path):
            new_to_dir = os.path.join(to_dir, file)
            if not os.path.exists(new_to_dir):
                os.makedirs(new_to_dir)
            generate_pages_recursively(from_path, template_path, new_to_dir)
        if file.endswith('.md'):
            to_path = os.path.join(to_dir, file.replace('.md', '.html'))
            generate_page(from_path, template_path, to_path)