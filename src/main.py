from textnode import TextNode
from htmlnode import HTMLNode, LeafNode
from helper import split_nodes_delimiter, text_to_textnodes

def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

    nodes = text_to_textnodes(text)

    print(f"------------- Here is my printing -------------")

    print(f"{len(nodes)}")
    
    for node in nodes:
        print(f"Node ---->TYPE:{node.text_type} \nTEXT:{node.text}<----")

    print(f"------------- Here is my printing -------------")

main()
