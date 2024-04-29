from textnode import TextNode
from htmlnode import HTMLNode, LeafNode
from helper import (split_nodes_delimiter, text_to_textnodes, markdown_to_blocks,
                    move_all_content)

def main():
    path_to_copy = "/Users/fercalatayud/Documents/Tech/workspace/github.com/FerCalatayud/static_site_generator/static"
    path_to_paste = "/Users/fercalatayud/Documents/Tech/workspace/github.com/FerCalatayud/static_site_generator/public"

    move_all_content(path_to_copy, path_to_paste)

main()
