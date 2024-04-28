from htmlnode import LeafNode
from textnode import TextNode
from enum import Enum
import re

class TextNodeType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextNodeType.TEXT:
        return LeafNode(text_node.text)
    elif text_node.text_type == TextNodeType.BOLD:
        return LeafNode(text_node.text, tag="b")
    elif text_node.text_type == TextNodeType.ITALIC:
        return LeafNode(text_node.text, tag="i")
    elif text_node.text_type == TextNodeType.CODE:
        return LeafNode(text_node.text, tag="code")
    elif text_node.text_type == TextNodeType.LINK:
        return LeafNode(text_node.text, tag="a", props={"href": text_node.url})
    elif text_node.text_type == TextNodeType.IMAGE:
        return LeafNode("", tag="img", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Text Node has no type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if text_type not in (item.value for item in TextNodeType):
            raise TypeError("You passed a wwrong delimiter to the function")

    for node in old_nodes:
        if node.text_type != 'text':
            new_nodes.append(node)
            continue

        text_list = node.text.split(delimiter)

        #if len(text_list) < 3:
        #    new_nodes.append(node)
        #    continue

        if len(text_list) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        for indx in range(0, len(text_list)):
            if len(text_list[indx]) == 0:
                continue
            elif indx % 2 != 0:
                new_nodes.append(TextNode(text_list[indx], text_type))
            else:
                new_nodes.append(TextNode(text_list[indx], "text"))
        
    return new_nodes

def extract_markdown_images(text):
    #r"!\[(.*?)\]\((.*?)\)"

    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    return matches

def extract_markdown_links(text):
    #r"\[(.*?)\]\((.*?)\)"

    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)

    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    

    for node in old_nodes:

        if node.text_type != 'text':
            new_nodes.append(node)
            continue
        elif node.text == "":
            continue

        image_tuples = extract_markdown_images(node.text)

        if len(image_tuples) == 0:
            new_nodes.append(node)
            continue

        text_to_split = node.text

        for img in image_tuples:
            node_splited = text_to_split.split(f"![{img[0]}]({img[1]})", 1)
            if len(node_splited) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            
            new_text_node = node_splited[0]
            text_to_split = node_splited[1]


            if new_text_node != "":
                new_nodes.append(TextNode(new_text_node, "text"))
                new_nodes.append(TextNode(img[0], "image", img[1]))
            else:
                new_nodes.append(TextNode(img[0], "image", img[1]))

        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, "text"))
        
    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:

        if node.text_type != 'text':
            new_nodes.append(node)
            continue
        elif node.text == "":
            continue

        link_tuples = extract_markdown_links(node.text)

        if len(link_tuples) == 0:
            new_nodes.append(node)
            continue

        text_to_split = node.text

        for link in link_tuples:
            node_splited = text_to_split.split(f"[{link[0]}]({link[1]})", 1)
            new_text_node = node_splited[0]
            text_to_split = node_splited[1]

            if new_text_node != "":
                new_nodes.append(TextNode(new_text_node, "text"))
                new_nodes.append(TextNode(link[0], "link", link[1]))
            else:
                new_nodes.append(TextNode(link[0], "link", link[1]))

        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, "text"))
        
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]

    for item in TextNodeType:
        if item.value == "text":
            continue
        elif item.value == "bold":
            nodes = split_nodes_delimiter(nodes, "**", item.value)
        elif item.value == "italic":
            nodes = split_nodes_delimiter(nodes, "*", item.value)
        elif item.value == "code":
            nodes = split_nodes_delimiter(nodes, "`", item.value)
        elif item.value == "link":
            nodes = split_nodes_image(nodes)
        elif item.value == "image":
            nodes = split_nodes_link(nodes)
    
    return nodes
