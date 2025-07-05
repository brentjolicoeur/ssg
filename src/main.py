import os, shutil
from generate_content import generate_pages_recursive

def main():
    clear_and_copy_directory('./static', './public')
    generate_pages_recursive('./content', './template.html', './public')

def clear_and_copy_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)

if __name__ == "__main__":
    main()