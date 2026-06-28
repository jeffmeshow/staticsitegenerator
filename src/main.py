import os
import argparse
from copystatic import clear_public_files, copy_static_files
from generatepage import generate_pages, get_files_r
from config import PUBLIC_DIR, STATIC_DIR, CONTENT_DIR

from textnode import TextNode, TextType

def main():
    clear_public_files(PUBLIC_DIR)
    copy_static_files(PUBLIC_DIR, STATIC_DIR)
    generate_pages(CONTENT_DIR, "template.html")



if __name__ == "__main__":
    main()