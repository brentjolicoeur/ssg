import os, shutil

from markdown_to_html import markdown_to_html_node


def main():
    clear_and_copy_directory('./static', './public')
    generate_page('./content/index.md', 'template.html', './public/index.html')

def clear_and_copy_directory(source_path, destination_path):
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    shutil.copytree(source_path, destination_path)

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith('# '):
            title = line.split(maxsplit=1)[1]
            return title.strip()
    raise Exception("Title header not found.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating a page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_text = f.read()

    content_node = markdown_to_html_node(markdown_text)

    html_content = content_node.to_html()

    title = extract_title(markdown_text)

    
    with open(template_path) as g:
        template_text = g.read()

    new_template = template_text.replace('{{ Title }}', title)
    new_template =new_template.replace('{{ Content }}', html_content)


    directories = os.path.dirname(dest_path)
    os.makedirs(directories, exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(new_template)

if __name__ == "__main__":
    main()