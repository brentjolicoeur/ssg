import os, shutil, sys
from generate_content import generate_pages_recursive

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = '/'
    clear_and_copy_directory('./static', './docs')
    generate_pages_recursive('./content', './template.html', './docs', basepath)

def clear_and_copy_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)

if __name__ == "__main__":
    main()