import sys

from shutil import rmtree
from distutils.dir_util import copy_tree
from os import *

from generate_page import generate_page, generate_pages_recursively

"""
def remove_public(path):
    path_to_public = path.join(path, "public")
    rmtree(path_to_public, ignore_errors=True)

def create_public(path: os.path = "."):
    path_to_public = path.join(path, "public")
    if not path.exists(path_to_public):
        makedirs(path_to_public)

def cp_static_to_public(path: os.path = "."):
    path_to_public = path.join(path, "public")
    path_to_static = path.join(path, "static")
    if not path.exists(path_to_static):
        makedirs(path_to_static)
    copy_tree(path_to_static, path_to_public)
"""


def main():

    if len(sys.argv) == 2:
        print("Argument passed: " + sys.argv[1])
        base_path = path.abspath(".") + sys.argv[1]
    else:
        base_path = path.abspath(".")
        print("No argument passed, using current directory: " + base_path)

    from_dir = path.abspath("content")
    template_path = path.abspath("template.html")
    to_dir = path.join(base_path, "public")

    rmtree(to_dir, ignore_errors=True)
    makedirs(to_dir)
    copy_tree(path.abspath("static"), to_dir)

    print(f'Generating into {to_dir}')

    generate_pages_recursively(from_dir, template_path, to_dir)

main()