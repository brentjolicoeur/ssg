import os, shutil

from generate_content import generate_pages_recursive, generate_page


def main():
    clear_and_copy_directory('./static', './public')
    #generate_page('./content/index.md', 'template.html', './public/index.html')
    generate_pages_recursive('./content', 'template.html', './public')

def clear_and_copy_directory(source_path, destination_path):
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    shutil.copytree(source_path, destination_path)

if __name__ == "__main__":
    main()