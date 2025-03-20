
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = [] if children is None else children #if children is not None else []
        self.props = {} if props is None else props #if props is not None else {}

    def to_html(self):
        """# Handle children
        children_html = "".join(child.to_html() for child in self.children if child is not None) if self.children else ""

        # Handle special cases (e.g., img or a tags)
        if self.tag is None:
            return children_html
        
        if self.value is not None:
            if self.tag == "img":
                return f'<{self.tag} src="{self.value}" alt="" />'  # Add alt attribute
            elif self.tag == "a":
                return f'<{self.tag} href="{self.value}">{children_html}</{self.tag}>'

        # Default case for generic tags
        return f"<{self.tag}>{children_html}</{self.tag}>"""

    def props_to_html(self):
        emptylist = [] # Prepare an empty list to collect HTML attributes
        if self.props is None: # Handle the case where `props` is None
            return ""
        for key, value in self.props.items(): # Loop through each key-value pair in props
            emptylist.append(f' {key}="{value}"') # Add the formatted string to the list
        return "".join(emptylist) # Join the list elements into a single string
    
    def __repr__(self):
        children_repr = None if not self.children else self.children
        props_repr = (
            "{"
            + ", ".join(f'"{key}": "{value}"' for key, value in self.props.items())
            + "}"
            if self.props
            else None
        )
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={children_repr}, props={props_repr})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
    # Call parent constructor with empty children list
        super().__init__(tag, value, None, props)

    def to_html(self):
        # Check if value exists
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        # If no tag, return raw text
        if self.tag is None:
            return self.value
        """props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>" """
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        # Otherwise, return formatted HTML

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        """if self.props:
            # Handle props/attributes
            props_str = ""
            for key, val in self.props.items():
                props_str += f' {key}="{val}"'
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>" """

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if props is None:
            props = {}
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise  ValueError("invalid HTML: no tag")
        if self.children is None:
            raise  ValueError("invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

        """# Start building the HTML string with the opening tag
        html = f"<{self.tag}"
        # Add properties if they exist
        if self.props:
            for prop_name, prop_value in self.props.items():
                html += f' {prop_name}="{prop_value}"'
        # Close the opening tag
        html += ">"
        # Iterate through each child and add its HTML
        for child in self.children:
        # Call to_html() on each child to get its HTML representation
            child_html = child.to_html()
            html += child_html
        # Add the closing tag
        html += f"</{self.tag}>"
        # Return the complete HTML string
        return html"""
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"