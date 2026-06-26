import os
import argparse

from textnode import TextNode, TextType

def main():
    node = TextNode("test", TextType.PLAIN, None)
    print(node)

if __name__ == "__main__":
    main()