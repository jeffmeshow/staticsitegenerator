import os
import argparse
from copystatic import clear_public_files, copy_static_files
from generatepage import generate_pages, get_files_r
from config import PUBLIC_DIR, STATIC_DIR, CONTENT_DIR

from textnode import TextNode, TextType

def main():

    #setup parser 
    parser = argparse.ArgumentParser(description="Static Site Generator:")
    parser.add_argument("basepath", type=str, help="Enter the base path to generate:")
    args = parser.parse_args()
    basepath: str = args.basepath
    if basepath == "":
        basepath = "/"    

    clear_public_files(PUBLIC_DIR)
    copy_static_files(PUBLIC_DIR, STATIC_DIR)
    generate_pages(CONTENT_DIR, "template.html", basepath)



if __name__ == "__main__":
    main()