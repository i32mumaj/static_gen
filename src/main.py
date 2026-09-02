from shutil import rmtree
from distutils.dir_util import copy_tree
from os import *

from generate_page import generate_page, generate_pages_recursively

def remove_public():
    path_to_public = path.abspath("public")
    rmtree(path_to_public, ignore_errors=True)

def create_public():
    path_to_public = path.abspath("public")
    if not path.exists(path_to_public):
        makedirs(path_to_public)

def cp_static_to_public():
    path_to_public = path.abspath("public")
    path_to_static = path.abspath("static")
    if not path.exists(path_to_static):
        makedirs(path_to_static)
    copy_tree(path_to_static, path_to_public)

def main():
    remove_public()
    create_public()
    cp_static_to_public()
    from_dir = path.abspath("content")
    template_path = path.abspath("template.html")
    to_dir = path.abspath("public")
    generate_pages_recursively(from_dir, template_path, to_dir)

main()