import os, shutil, sys

from generate_content import generate_pages_recursive, generate_page


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = '/'
    clear_and_copy_directory('./static', './docs')
    generate_pages_recursive('./content', 'template.html', './docs', basepath)

def clear_and_copy_directory(source_path, destination_path):
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    shutil.copytree(source_path, destination_path)

if __name__ == "__main__":
    main()