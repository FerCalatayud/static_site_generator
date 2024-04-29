import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode
from helper import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links, 
                    split_nodes_image, split_nodes_link, text_to_textnodes,
                    markdown_to_blocks, block_to_block_type, extract_title)


class TestHTMLNode(unittest.TestCase):

    # =================================================================
    # ------------ TEST HTML NODE ------------
    # =================================================================

    def test_to_html(self):
        node = HTMLNode()

        with self.assertRaises(NotImplementedError):
            node.to_html()
        
    def test_props_to_html(self):
        node_2 = HTMLNode(tag="p", 
                        value="Hellow, World!", 
                        children=None, 
                        props={"href": "https://www.google.com", "target": "_blank"})

        html_props = node_2.props_to_html()
        if html_props != "href=https://www.google.com target=_blank":
            return None
        
    # =================================================================
    # ------------ TEST LEAF NODE ------------
    # =================================================================

    def test_lead_node_value(self):
        with self.assertRaises(TypeError):       
            LeafNode()

    def test_leaf_node_to_html_no_tag(self):
        value = "This is the value"
        ln = LeafNode(value)

        self.assertEqual(ln.to_html(), value)
    
    def test_leaf_node_to_html_correct_tag(self):
        value = "This is the value"
        value_with_tag = "<p>This is the value</p>"
        ln = LeafNode(value, tag="p")

        self.assertEqual(ln.to_html(), value_with_tag)

    # =================================================================
    # ------------ TEST PARENT NODE ------------
    # =================================================================

    def test_parent_node_children(self):
        with self.assertRaises(TypeError):       
            ParentNode(tag="p")
    
    def test_parent_node_tag(self):
        value = "This is the value"
        with self.assertRaises(TypeError):       
            ParentNode(LeafNode(value, tag="p"))
    
    def test_leaf_node_to_html_only_children(self):
        node = ParentNode(
                        "p",
                        [
                            LeafNode("Bold text", "b"),
                            LeafNode("Normal text", None),
                            LeafNode("italic text", "i"),
                            LeafNode("Normal text", None),
                        ],
                    )
        
        result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        self.assertEqual(node.to_html(), result)
    
    def test_leaf_node_to_html_parents_and_children(self):
        node = ParentNode(
                        "p",
                        [
                            LeafNode("Bold text", "b"),
                            LeafNode("Normal text", None),
                            ParentNode("z", [LeafNode("Bold text", "b")]),
                            LeafNode("italic text", "i"),
                            LeafNode("Normal text", None),
                            ParentNode("z", [LeafNode("Bold text", "b"), LeafNode("Normal text", None)])
                        ],
                    )
        
        result = "<p><b>Bold text</b>Normal text<z><b>Bold text</b></z><i>italic text</i>Normal text<z><b>Bold text</b>Normal text</z></p>"

        self.assertEqual(node.to_html(), result)

    def test_leaf_node_to_html_parents_and_children_and_grandchildren(self):
        node = ParentNode(
                        "p",
                        [
                            LeafNode("Bold text", "b"),
                            LeafNode("Normal text", None),
                            ParentNode("z", [LeafNode("Bold text", "b")]),
                            LeafNode("italic text", "i"),
                            LeafNode("Normal text", None),
                            ParentNode("z", [LeafNode("Bold text", "b"), ParentNode("z", [LeafNode("Bold text", "b")])])
                        ],
                    )
        
        result = "<p><b>Bold text</b>Normal text<z><b>Bold text</b></z><i>italic text</i>Normal text<z><b>Bold text</b><z><b>Bold text</b></z></z></p>"

        self.assertEqual(node.to_html(), result)
    
    # =================================================================
    # ------------ TEST helper functions ------------
    # =================================================================

    def test_split_nodes_delimiter_wrong_type(self):
        node_1 = TextNode("This is the first node", "cpp")
        node_2 = TextNode("This is the second node", "text")
        #node_3 = TextNode("This is the *third node*", "text")
        #node_4 = TextNode("This is the **forth node** and it has more text", "text")
        #node_5 = TextNode("This is the `fifth node` and it has `more text`", "text")
        
        with self.assertRaises(TypeError):       
            split_nodes_delimiter([node_1, node_2], "*", "cpp")
    
    def test_split_nodes_delimiter_no_delimiter(self):
        #node_1 = TextNode("This is the first node", "cpp")
        node_2 = TextNode("This is the second node", "text")
        #node_3 = TextNode("This is the *third node*", "text")
        #node_4 = TextNode("This is the **forth node** and it has more text", "text")
        #node_5 = TextNode("This is the `fifth node` and it has `more text`", "text")
        
        self.assertEqual(split_nodes_delimiter([node_2], "*", "bold"), [node_2])

    def test_split_nodes_delimiter_with_delimiter(self):
        #node_1 = TextNode("This is the first node", "cpp")
        #node_2 = TextNode("This is the second node", "text")
        node_3 = TextNode("This is the *third node*", "text")
        #node_4 = TextNode("This is the **forth node** and it has more text", "text")
        #node_5 = TextNode("This is the `fifth node` and it has `more text`", "text")

        
        self.assertEqual(split_nodes_delimiter([node_3], "*", "bold"), [TextNode("This is the ", "text"), 
                                                                        TextNode("third node", "bold")])
    
    def test_split_nodes_delimiter_with_delimiter_2(self):
        #node_1 = TextNode("This is the first node", "cpp")
        #node_2 = TextNode("This is the second node", "text")
        node_3 = TextNode("This is the *third node*", "text")
        node_4 = TextNode("This is the *forth node* and it has more text", "text")
        #node_5 = TextNode("This is the `fifth node` and it has `more text`", "text")

        
        self.assertEqual(split_nodes_delimiter([node_3, node_4], "*", "bold"), [TextNode("This is the ", "text"), 
                                                                        TextNode("third node", "bold"),
                                                                        TextNode("This is the ", "text"),
                                                                        TextNode("forth node", "bold"),
                                                                        TextNode(" and it has more text", "text")])
    
    def test_split_nodes_delimiter_with_delimiter_3(self):
        #node_1 = TextNode("This is the first node", "cpp")
        #node_2 = TextNode("This is the second node", "text")
        node_3 = TextNode("This is the *third node*", "text")
        node_4 = TextNode("This is the *forth node* and it has more text", "text")
        #node_5 = TextNode("This is the `fifth node` and it has `more text`", "text")
        node_6 = TextNode("This is the *sixth node* and *it* has more *text*, than others", "text")

        
        self.assertEqual(split_nodes_delimiter([node_3, node_4, node_6], "*", "bold"), [TextNode("This is the ", "text"), 
                                                                        TextNode("third node", "bold"),
                                                                        TextNode("This is the ", "text"),
                                                                        TextNode("forth node", "bold"),
                                                                        TextNode(" and it has more text", "text"),
                                                                        TextNode("This is the ", "text"),
                                                                        TextNode("sixth node", "bold"),
                                                                        TextNode(" and ", "text"),
                                                                        TextNode("it", "bold"),
                                                                        TextNode(" has more ", "text"),
                                                                        TextNode("text", "bold"),
                                                                        TextNode(", than others", "text")])
    
    def test_split_nodes_delimiter_with_delimiter_4(self):
        #node_1 = TextNode("This is the first node", "cpp")
        #node_2 = TextNode("This is the second node", "text")
        #node_3 = TextNode("This is the *third node*", "text")
        #node_4 = TextNode("This is the *forth node* and it has more text", "text")
        node_5 = TextNode("This is the `fifth node` and it has `more text`", "text")
        #node_6 = TextNode("This is the *sixth node* and *it* has more *text*, than others", "text")

        
        self.assertEqual(split_nodes_delimiter([node_5], "`", "code"), [TextNode("This is the ", "text"),
                                                                        TextNode("fifth node", "code"),
                                                                        TextNode(" and it has ", "text"),
                                                                        TextNode("more text", "code")
                                                                        ])
        
    def test_split_nodes_delimiter_with_delimiter_5(self):
        #node_1 = TextNode("This is the first node", "cpp")
        #node_2 = TextNode("This is the second node", "text")
        #node_3 = TextNode("This is the *third node*", "text")
        #node_4 = TextNode("This is the *forth node* and it has more text", "text")
        node_5 = TextNode("`This is the `fifth node` and it has `more text`", "text")
        #node_6 = TextNode("This is the *sixth node* and *it* has more *text*, than others", "text")

        with self.assertRaises(ValueError):       
            split_nodes_delimiter([node_5], "`", "code")

    # =================================================================
    # ------------ TEST helper functions REGEX ------------
    # =================================================================

    def test_regex_find_images_url_and_anchor(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"

        matches = extract_markdown_images(text)

        expected_result = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]

        self.assertEqual(matches, expected_result)

    def test_regex_find_links_and_anchor(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

        matches = extract_markdown_links(text)

        expected_result = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]

        self.assertEqual(matches, expected_result)

    def test_regex_find_links_and_anchor_2(self):
        text = "This is text with a link](https://www.example.com) and [another](https://www.example.com/another)"

        matches = extract_markdown_links(text)

        expected_result = [("another", "https://www.example.com/another")]

        self.assertEqual(matches, expected_result)
    
    # =================================================================
    # ------------ TEST helper functions SPLIT IMAGE NODES ------------
    # =================================================================

    def test_split_nodes_with_images(self):
        nodes = [TextNode(
    "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
    "text",)]

        matches = split_nodes_image(nodes)

        expected_result = [
    TextNode("This is text with an ", "text"),
    TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    TextNode(" and another ", "text"),
    TextNode(
        "second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
    ),
]


        self.assertEqual(matches, expected_result)
    
    def test_split_nodes_with_images_2(self):
        nodes = [TextNode(
    "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and this is at the end",
    "text",)]

        matches = split_nodes_image(nodes)

        expected_result = [
    TextNode("This is text with an ", "text"),
    TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    TextNode(" and another ", "text"),
    TextNode(
        "second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
    ),
    TextNode(" and this is at the end", "text")
]


        self.assertEqual(matches, expected_result)
    
    def test_split_nodes_with_images_3(self):
        nodes = [TextNode(
    "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) that was an image and here is another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and this is at the end",
    "text",)]

        matches = split_nodes_image(nodes)

        expected_result = [
    TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    TextNode(" that was an image and here is another ", "text"),
    TextNode(
        "second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
    ),
    TextNode(" and this is at the end", "text")
]


        self.assertEqual(matches, expected_result)
    
    def test_split_nodes_with_images_4(self):
        nodes = [TextNode(
    "[image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) that was an image and here is another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and this is at the end",
    "text",)]

        matches = split_nodes_image(nodes)

        expected_result = [
    TextNode("[image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) that was an image and here is another ", "text"),
    TextNode(
        "second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
    ),
    TextNode(" and this is at the end", "text")
]


        self.assertEqual(matches, expected_result)

    # TODO
    # it might be missing a test for when the image tag is not closed but I already tried and didn't find
    # a case where that happens. The solution does test for ir in the code but don't know when that is the case becase
    # the function that substracts the images would not return the images and there fore never get to that case in code.

    # =================================================================
    # ------------ TEST helper functions SPLIT LINK NODES ------------
    # =================================================================

    def test_split_nodes_with_links(self):
        nodes = [TextNode(
    "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
    "text",)]

        matches = split_nodes_link(nodes)

        expected_result = [
    TextNode("This is text with a ", "text"),
    TextNode(
        "link", "link", "https://www.example.com"
    ),
    TextNode(" and ", "text"),
    TextNode(
        "another", "link", "https://www.example.com/another"
    ),
]

        self.assertEqual(matches, expected_result)

    # =================================================================
    # ------------ TEST helper functions CONVERT MARKDOWN TEXT INTO NODES ------------
    # =================================================================

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        
        expected_result = [
                    TextNode("This is ", "text"),
                    TextNode("text", "bold"),
                    TextNode(" with an ", "text"),
                    TextNode("italic", "italic"),
                    TextNode(" word and a ", "text"),
                    TextNode("code block", "code"),
                    TextNode(" and an ", "text"),
                    TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and a ", "text"),
                    TextNode("link", "link", "https://boot.dev"),
                ]


        nodes = text_to_textnodes(text)

        self.assertEqual(nodes, expected_result)
    
    def test_text_to_textnodes_2(self):
        text = "This is **text** with an *italic* word *and* a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        
        expected_result = [
                    TextNode("This is ", "text"),
                    TextNode("text", "bold"),
                    TextNode(" with an ", "text"),
                    TextNode("italic", "italic"),
                    TextNode(" word ", "text"),
                    TextNode("and", "italic"),
                    TextNode(" a ", "text"),
                    TextNode("code block", "code"),
                    TextNode(" and an ", "text"),
                    TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and a ", "text"),
                    TextNode("link", "link", "https://boot.dev"),
                ]


        nodes = text_to_textnodes(text)

        self.assertEqual(nodes, expected_result)

    def test_text_to_textnodes_3(self):
        text = "This is **text* with an *italic* word *and* a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

        with self.assertRaises(ValueError):       
            text_to_textnodes(text)

    def test_markdown_to_blocks(self):
        markdown_text = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"

        expected_result = ["This is **bolded** paragraph\n", 
                           "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n",
                           "* This is a list\n* with items"]

        blocks = markdown_to_blocks(markdown_text)

        self.assertEqual(blocks, expected_result)

    def test_markdown_to_blocks_2(self):
        markdown_text = "This is **bolded** paragraph\n\n\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"

        expected_result = ["This is **bolded** paragraph\n", 
                           "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n",
                           "* This is a list\n* with items"]

        blocks = markdown_to_blocks(markdown_text)

        self.assertEqual(blocks, expected_result)

    # =================================================================
    # ------------ TEST helper functions CHECK THE BLOCK TYPE ------------
    # =================================================================

    def test_block_to_block_type(self):
        block = "* This is a list\n* with items"
        
        expected_result = "unordered_list"

        actual_result = block_to_block_type(block)

        self.assertEqual(actual_result, expected_result)

    def test_block_to_block_type_2(self):
        block = "* This is a list\n with items"
        
        expected_result = "paragraph"

        actual_result = block_to_block_type(block)

        self.assertEqual(actual_result, expected_result)

    def test_block_to_block_type_3(self):
        block = "#### This is a list with items"
        
        expected_result = "heading"

        actual_result = block_to_block_type(block)

        self.assertEqual(actual_result, expected_result)

    def test_block_to_block_type_4(self):
        block = "> This is a list with items"
        
        expected_result = "quote"

        actual_result = block_to_block_type(block)

        self.assertEqual(actual_result, expected_result)

    def test_block_to_block_type_5(self):
        block = "```This is a list with items\nwith code```"
        
        expected_result = "code"

        actual_result = block_to_block_type(block)

        self.assertEqual(actual_result, expected_result)

    def test_block_to_block_type_6(self):
        block = "1. This is a list\n2. with items\n3. and items"
        
        expected_result = "ordered_list"

        actual_result = block_to_block_type(block)

        self.assertEqual(actual_result, expected_result)

    def test_block_to_block_type_7(self):
        block = "1. This is a list\n3. with items\n3. and items"
        
        expected_result = "paragraph"

        actual_result = block_to_block_type(block)

        self.assertEqual(actual_result, expected_result)

    # =================================================================
    # ------------ TEST helper functions CHECK IF MARKDOWN HAS TITLE ------------
    # =================================================================

    def test_markdown_has_title(self):
        markdown = """###### The Unparalleled Majesty of "The Lord of the Rings"

                        [Back Home](/)

                        ![LOTR image artistmonkeys](/images/rivendell.png)

                        > "I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
                        > I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
                        > I think that many confuse 'applicability' with 'allegory'; but the one resides in the freedom of the reader, and the other in the purposed domination of the author."
                        """
        
        expected_result = '###### The Unparalleled Majesty of "The Lord of the Rings"'

        result = extract_title(markdown)

        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()