from htmlnode import LeafNode, HTMLNode, ParentNode
from textnode import TextNode
from enum import Enum
import re
import os
import shutil

class TextNodeType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextNodeType.TEXT.value:
        return LeafNode(text_node.text)
    elif text_node.text_type == TextNodeType.BOLD.value:
        return LeafNode(text_node.text, tag="b")
    elif text_node.text_type == TextNodeType.ITALIC.value:
        return LeafNode(text_node.text, tag="i")
    elif text_node.text_type == TextNodeType.CODE.value:
        return LeafNode(text_node.text, tag="code")
    elif text_node.text_type == TextNodeType.LINK.value:
        return LeafNode(text_node.text, tag="a", props={"href": text_node.url})
    elif text_node.text_type == TextNodeType.IMAGE.value:
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

def markdown_to_blocks(markdown_text):

    blocks = list(map(lambda s: s.strip(), filter(lambda s: s if s != "" else False, markdown_text.split("\n\n"))))

    #total_blocks = len(blocks)

    '''for indx in range(0, total_blocks):
        if indx < total_blocks - 1:
            blocks[indx] += "\n"'''
    
    """blocks = markdown_text.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks"""

    return blocks

def block_to_block_type(block):

    lines = block.split("\n")

    if re.findall(r"^(#{1,6}\s)", block):
        return BlockType.HEADING.value
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE.value
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH.value
        return BlockType.QUOTE.value
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH.value
        return BlockType.UNORDERED_LIST.value
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH.value
        return BlockType.UNORDERED_LIST.value
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH.value
            i += 1
        return BlockType.ORDERED_LIST.value
    return BlockType.PARAGRAPH.value

def paragraph_block_to_html(block):
    
    text_nodes = []
    html_nodes = []

    block_type = block_to_block_type(block)
    if block_type != "paragraph":
            raise ValueError("Wrong type block for this function")

    lines_in_block = block.split("\n")
    paragraph = " ".join(lines_in_block)

    text_nodes = text_to_textnodes(paragraph)
    
    for node in text_nodes:
       html_nodes.append(text_node_to_html_node(node))

    return ParentNode(tag="p", children=html_nodes)

def heading_block_to_html(block):

    heading_symbol = re.search(r"^(#{1,6}\s)", block)

    if not heading_symbol:
        raise ValueError("Wrong type block for this function")
    
    heading_symbol_string = heading_symbol.group(0).strip()
        
    formated_line = re.sub(r"^(#{1,6}\s)", "", block).strip()
    text_nodes = text_to_textnodes(formated_line)
    html_node = []

    for node in text_nodes:
        html_node.append(text_node_to_html_node(node))

    #print(f"----->{formated_line}<-------")

    return ParentNode(tag=f"h{len(heading_symbol_string)}", children=html_node)

def code_block_to_html(block):
    text_nodes = []
    html_nodes = []
        
    if block.startswith("```") and block.endswith("```"):
        text_nodes = text_to_textnodes(block.strip("```").strip("\n"))

    else:
        raise ValueError("Wrong type block for this function")
    
    for node in text_nodes:
       html_nodes.append(text_node_to_html_node(node))

    code_html = ParentNode(tag="code", children=html_nodes)

    return ParentNode(tag="pre", children=[code_html])

def quote_block_to_html(block):
    
    lines_in_block = block.split("\n")
    formated_lines = []
    html_nodes = []

    for line in lines_in_block:
        if not line.startswith(">"):
            raise ValueError("Wrong type block for this function")
        
        formated_lines.append(line.lstrip(">").strip())

    text_nodes = text_to_textnodes(" ".join(formated_lines))
    
    for node in text_nodes:
       html_nodes.append(text_node_to_html_node(node))

    return ParentNode(tag="blockquote", children=html_nodes)

def unordered_list_block_to_html(block):
    
    lines_in_block = block.split("\n")
    text_nodes = []
    html_nodes = []

    for line in lines_in_block:
        html_li_nodes = []
        if not line.startswith("- "):
            raise ValueError("Wrong type block for this function")
        
        formated_line = line.lstrip("- ").strip()
        text_nodes = text_to_textnodes(formated_line)
        for node in text_nodes:
            html_li_nodes.append(text_node_to_html_node(node))
        
        html_nodes.append(ParentNode(tag="li", children=html_li_nodes))

    return ParentNode(tag="ul", children=html_nodes)

def ordered_list_block_to_html(block):
    
    lines_in_block = block.split("\n")
    text_nodes = []
    html_nodes = []

    for indx in range(0, len(lines_in_block)):
        html_li_nodes = []
        if not lines_in_block[indx].startswith(f"{indx + 1}. "):
            raise ValueError("Wrong type block for this function")
        
        formated_line = lines_in_block[indx].lstrip(f"{indx + 1}. ").strip()
        text_nodes = text_to_textnodes(formated_line)
        for node in text_nodes:
            html_li_nodes.append(text_node_to_html_node(node))
        
        html_nodes.append(ParentNode(tag="li", children=html_li_nodes))

    return ParentNode(tag="ol", children=html_nodes)

def block_to_html(block):
    block_type = block_to_block_type(block)
    if block_type == "paragraph":
        return paragraph_block_to_html(block)
    if block_type == "heading":
        return heading_block_to_html(block)
    if block_type == "code":
        return code_block_to_html(block)
    if block_type == "quote":
        return quote_block_to_html(block)
    if block_type == "unordered_list":
        return unordered_list_block_to_html(block)
    if block_type == "ordered_list":
        return ordered_list_block_to_html(block)
    raise ValueError("Wrong block type")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    html_nodes = []

    for block in blocks:
        html_nodes.append(block_to_html(block))
    
    return ParentNode("div", children=html_nodes)

def move_all_content(path_to_copy, path_to_paste):
    print(f"======= Copy files and dirs from ----->{path_to_copy}<----- to ------>{path_to_paste}<------- =======")
    if not os.path.exists(path_to_copy):
        raise ValueError("Path provided doesn't exist")
    
    if not os.path.exists(path_to_paste):
        print(f"----> Creating dir ---->{path_to_paste}")
        os.mkdir(path_to_paste)

    dirs_to_copy = os.listdir(path_to_copy)
    print(f"----> On ---->{path_to_copy}<--- list of dirs and files --->{dirs_to_copy}")

    for dir in dirs_to_copy:
        current_dirs_to_copy = os.path.join(path_to_copy, dir)
        current_dir_to_paste = os.path.join(path_to_paste, dir)
        print(f"----> ON dir ---->{current_dirs_to_copy}")
        if os.path.isfile(current_dirs_to_copy):
            shutil.copy(current_dirs_to_copy, current_dir_to_paste)
            print(f"----> Copied file ----> {dir} <----- from ---->{current_dirs_to_copy}<--- to --->{current_dir_to_paste}")
            
        else:
            print(f"----> Recursion from ------>{path_to_copy}<------- to  ------>{current_dirs_to_copy}<-------")
            move_all_content(current_dirs_to_copy, current_dir_to_paste)
    
def extract_title(markdown):
    title_line = markdown.split("\n")[0]
    #if re.search(r"^(#{1,6}\s)", title_line):
    if title_line[0:2] == "# ":
        return title_line
    else:
        raise ValueError("This markdown page doesn't have a title")

def generate_page(from_path, template_path, dest_path):
    # Print the action to do on this program
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # go up a dir from src
    #from_path = f"../{from_path}"
    #dest_path = f"../{dest_path}"
    #template_path = f"../{template_path}"

    # open the markdown file
    with open(from_path) as markdown_file:
        file_markdown = markdown_file.read()
        
    # open the template file
    with open(template_path) as template_file:
        file_template = template_file.read()

    # convert markdown to html nodes
    makrdown_html = markdown_to_html_node(file_markdown)
    makrdown_html_string= makrdown_html.to_html()

    # extract title
    page_title = extract_title(file_markdown)

    # replace title and content on template
    new_html = file_template.replace("{{ Title }}", page_title)
    new_html = new_html.replace("{{ Content }}", makrdown_html_string)
    
    # write the html stirng into a file on dest_path and create the necesary directories
    dest_path_dir = os.path.dirname(dest_path)
    if dest_path_dir != "":
        os.makedirs(dest_path_dir, exist_ok=True)

    with open(dest_path, 'w') as index_file:
        index_file.write(new_html)

    print("JOB DONE, THANKS FOR TRUSTING ME WITH THE WORK.")
    