class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Not yet")

    def props_to_html(self):
        if self.props is None:
            return ""

        html_props = " ".join(map(lambda item: f" {item[0]}={item[1]}", self.props.items()))

        return html_props

    def __repr__(self) -> str:
        print(f"tag: {self.tag}")
        print(f"value: {self.value}")
        print(f"children: {self.children}")
        print(f"props: {self.props}")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__()
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("A parent node must have a tag")
        
        if self.children is None:
            raise ValueError("A parent node must have children")
        
        html_string = ""

        for child in self.children:
            # base case - leaf node            
            # call  itself
            # reduction
            html_string += child.to_html()      

        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
    def __eq__(self, other_object) -> bool:

        if not isinstance(other_object, ParentNode):
            return NotImplemented

        if len(self.children) != len(other_object.children):
            return False
        
        # Recursive comparison of each element in the children list
        return (self.tag == other_object.tag and
                self.props == other_object.props and
                len(self.children) == len(other_object.children) and
                all(s1 == s2 for s1, s2 in zip(self.children, other_object.children)))

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None) -> None:
        super().__init__()
        self.value = value
        self.tag = tag
        self.props = props

    def to_html(self):
        if self.value is None:
            raise ValueError("An HTML element needs a value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return NotImplemented
        return self.value == other.value and self.tag == other.tag and self.props == other.props
