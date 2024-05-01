# Python
import os
import shutil

# Internal
from helper import (move_all_content, generate_pages_recursive)

def main():

    path_static_dir = "./static"
    path_public_dir = "./public"
    path_content_dir = "./content"
    path_template = "./template.html"

    if os.path.exists(path_public_dir):
        shutil.rmtree(path_public_dir)

    move_all_content(path_static_dir, path_public_dir)

    generate_pages_recursive(path_content_dir, path_template, path_public_dir)

    print("JOB DONE, THANKS FOR TRUSTING ME WITH THE WORK.")

main()
