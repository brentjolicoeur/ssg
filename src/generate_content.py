import os

from markdown_funcs import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith('# '):
            title = line.split(maxsplit=1)[1]
            return title.strip()
    raise Exception("Title header not found.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating a page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_content = f.read()

    content_node = markdown_to_html_node(markdown_content)

    html_content = content_node.to_html()

    title = extract_title(markdown_content)

    
    with open(template_path) as g:
        template_text = g.read()

    new_template = template_text.replace('{{ Title }}', title)
    new_template =new_template.replace('{{ Content }}', html_content)
    new_template = new_template.replace('href="/', f'href="{basepath}')
    new_template = new_template.replace('src="/', f'src="{basepath}')

    directories = os.path.dirname(dest_path)
    os.makedirs(directories, exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(new_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    contents = os.listdir(dir_path_content)

    for item in contents:
        item_path = os.path.join(dir_path_content, item)

        if item.endswith('.md'):
            destination_path = item_path.replace('content', 'docs', 1)
            destination_path = destination_path.replace('.md', '.html')
            generate_page(item_path, template_path, destination_path, basepath)
        else:
            if os.path.isdir(item_path):
                generate_pages_recursive(item_path, template_path, dest_dir_path, basepath)