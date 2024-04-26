import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # ------------ TEST HTML NODE ------------
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
        
    # ------------ TEST LEAF NODE ------------
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

    # ------------ TEST PARENT NODE ------------
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

if __name__ == "__main__":
    unittest.main()