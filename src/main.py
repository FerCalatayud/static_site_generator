from textnode import TextNode
from htmlnode import HTMLNode, LeafNode
from helper import split_nodes_delimiter, text_to_textnodes, markdown_to_blocks

def main():
    markdown_text = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"

    blocks = markdown_to_blocks(markdown_text)

    print(f"------------- Here is my printing -------------")

    print(f"{len(blocks)}")
    
    for b in blocks:
        print(f"{b}")

    print(f"------------- Here is my printing -------------")

main()
