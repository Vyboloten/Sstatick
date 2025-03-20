import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Set up a node with props
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        # Act by calling props_to_html
        result = node.props_to_html()
        # Assert the output matches the expected result
        self.assertEqual(result, ' href="https://example.com" target="_blank"')

    def test_repr(self):
        # Set up a node with full attributes
        node = HTMLNode(tag="div", value="Hello", children=None, props={"id": "main"})
        # Act and Assert that __repr__ returns the correct string
        self.assertEqual(repr(node), 'HTMLNode(tag=div, value=Hello, children=None, props={"id": "main"})')

    def test_default_constructor(self):
    # Create a node without providing any arguments
        node = HTMLNode()
    # Assert that all attributes are their default values
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])  # Should initialize as an empty list
        self.assertEqual(node.props, {})  # Should initialize as an empty dictionary

    def test_props_to_html_empty(self): #Check how the props_to_html method handles the case when props is empty.
    # Create a node with no props
        node = HTMLNode(tag="div", props={})
    # Act
        result = node.props_to_html()
    # Assert that the result is an empty string (no space!)
        self.assertEqual(result, '')

    def test_multiple_children(self): #Test how the HTMLNode handles a children list containing multiple HTMLNode objects.
    # Set up a parent node with two children
        child1 = HTMLNode(tag="p", value="Paragraph 1")
        child2 = HTMLNode(tag="p", value="Paragraph 2")
        parent = HTMLNode(tag="div", children=[child1, child2])
    # Assert that the children were set correctly
        self.assertEqual(parent.children[0].value, "Paragraph 1")
        self.assertEqual(parent.children[1].value, "Paragraph 2")
    
    def test_to_html_raises(self):
    # Correct the instantiation of the HTMLNode
        node = HTMLNode(tag="div")
    # Assert that calling to_html raises a NotImplementedError
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_props_only(self): #Ensure that an HTMLNode with only props behaves as expected.
    # Set up a node with props but no value or children
        node = HTMLNode(tag="a", props={"href": "https://example.com", "target": "_blank"})
    # Assert attributes
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"href": "https://example.com", "target": "_blank"}) 
    # Assert props_to_html works
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_children_only(self): #Test the structure of a node that has children but no value or props.
    # Create child nodes
        child1 = HTMLNode(tag="p", value="Child 1")
        child2 = HTMLNode(tag="p", value="Child 2")
    # Create parent with children
        parent = HTMLNode(tag="div", children=[child1, child2])
    # Assert attributes
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.value, None)
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].value, "Child 1")
        self.assertEqual(parent.children[1].tag, "p")
    # Assert __repr__ shows children correctly
        self.assertIn("Child 1", repr(parent))
    
    def test_empty_node(self): #Test that an HTMLNode created without any arguments is structured as expected.
    # Create an empty node
        node = HTMLNode()
    # Assert all attributes use default values
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})
    # Assert __repr__ reflects the default state
        self.assertEqual(
        repr(node),
        "HTMLNode(tag=None, value=None, children=None, props=None)"
    )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            [], #or none
        )
        self.assertEqual(
            node.props,
            {}, #or none
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_tag(self): #Test a leaf node with no tag (should return raw text):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_with_props(self): #Test a leaf node with properties/attributes:
        node = LeafNode("a", "Click me!", {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">Click me!</a>')

    def test_leaf_no_value(self): #Test error handling when no value is provided:
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_different_tags(self): #Test different HTML tags:
        b_node = LeafNode("b", "Bold text")
        self.assertEqual(b_node.to_html(), "<b>Bold text</b>")
        
        img_node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(img_node.to_html(), '<img src="image.jpg" alt="An image"></img>')

    def test_leaf_with_special_characters(self): #How your implementation handles special characters
        node = LeafNode("p", "Text with <special> & \"characters\"")
        self.assertEqual(node.to_html(), "<p>Text with <special> & \"characters\"</p>")

    def test_leaf_empty_string_value(self): #Empty string values (which should be valid, unlike None)
        node = LeafNode("span", "")
        self.assertEqual(node.to_html(), "<span></span>")

    def test_leaf_with_numeric_value(self): #Numeric values (which might be converted to strings)
        node = LeafNode("div", "12345")
        self.assertEqual(node.to_html(), "<div>12345</div>")

    def test_leaf_h1_tag(self): #Different HTML tags like h1
        node = LeafNode("h1", "Page Title")
        self.assertEqual(node.to_html(), "<h1>Page Title</h1>")

    def test_leaf_with_class_prop(self): #Class attributes commonly used in HTML
        node = LeafNode("div", "Content", {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container">Content</div>')

    def test_leaf_with_data_attributes(self): #Data attributes which are common in modern web development
        node = LeafNode("button", "Click Me", {"data-id": "123", "data-action": "submit"})
        self.assertEqual(node.to_html(), '<button data-id="123" data-action="submit">Click Me</button>')

class TestParentNode(unittest.TestCase):
    def test_basic_parent_node(self): # Test a basic parent with one leaf child
        child = LeafNode("b", "Bold text")
        parent = ParentNode("p", [child])
        self.assertEqual(parent.to_html(), "<p><b>Bold text</b></p>")
    
    def test_parent_with_multiple_children(self): # Test a parent with multiple leaf children
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text")
        ]
        parent = ParentNode("p", children)
        self.assertEqual(parent.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i></p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_nested_parent_nodes(self): # Test nested parent nodes (parent containing another parent)
        grandchild = LeafNode("span", "Grandchild text")
        child = ParentNode("div", [grandchild])
        parent = ParentNode("section", [child])
        self.assertEqual(parent.to_html(), "<section><div><span>Grandchild text</span></div></section>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_with_props(self): # Test a parent node with properties
        child = LeafNode("p", "Paragraph text")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        # Note: The order of properties might vary, so this test might need adjustment
        self.assertTrue("<div class=\"container\" id=\"main\">" in parent.to_html() or 
                    "<div id=\"main\" class=\"container\">" in parent.to_html())
        self.assertTrue(parent.to_html().endswith("<p>Paragraph text</p></div>"))

    def test_missing_tag_raises_error(self): # Test that a ValueError is raised when tag is None
        parent = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_missing_children_raises_error(self): # Test that a ValueError is raised when children is None
    # This might not be directly testable if children is a required parameter,
    # but you could modify the object after creation
        parent = ParentNode("div", [])
        parent.children = None
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_complex_nested_structure(self): # Test a complex nested structure
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode("i", "Italic")
        leaf3 = LeafNode(None, "Plain")
        inner_parent1 = ParentNode("span", [leaf1, leaf2])
        inner_parent2 = ParentNode("p", [leaf3])
        outer_parent = ParentNode("div", [inner_parent1, inner_parent2], {"class": "wrapper"})
        
        expected = '<div class="wrapper"><span><b>Bold</b><i>Italic</i></span><p>Plain</p></div>'
        # Since property order might vary
        actual = outer_parent.to_html()
        self.assertTrue('<div class="wrapper">' in actual or actual.startswith('<div '))
        self.assertTrue('<span><b>Bold</b><i>Italic</i></span>' in actual)
        self.assertTrue('<p>Plain</p>' in actual)
        self.assertTrue(actual.endswith('</div>'))

    def test_mixed_node_types(self): # Test parent with mix of leaf nodes and parent nodes
        leaf1 = LeafNode("em", "Emphasized")
        inner_parent = ParentNode("strong", [LeafNode(None, "Nested")])
        leaf2 = LeafNode(None, "Plain text")
        
        parent = ParentNode("div", [leaf1, inner_parent, leaf2])
        expected = '<div><em>Emphasized</em><strong>Nested</strong>Plain text</div>'
        self.assertEqual(parent.to_html(), expected)

    def test_parent_with_deeply_nested_structure(self): # Test a deeply nested structure (3+ levels)
        deepest = LeafNode("code", "print('Hello')")
        deep = ParentNode("pre", [deepest])
        middle = ParentNode("div", [deep], {"class": "code-block"})
        outer = ParentNode("section", [middle], {"id": "examples"})
        
        html = outer.to_html()
        self.assertTrue("<section" in html and "id=\"examples\"" in html)
        self.assertTrue("<div" in html and "class=\"code-block\"" in html)
        self.assertTrue("<pre><code>print('Hello')</code></pre>" in html)

    def test_parent_with_multiple_props(self): # Test a parent with multiple properties
        props = {
            "id": "main",
            "class": "container",
            "data-test": "true",
            "aria-label": "Main content"
        }
        parent = ParentNode("main", [LeafNode("p", "Content")], props)
        html = parent.to_html()
        
        # Check that all properties are included
        for prop, value in props.items():
            self.assertTrue(f'{prop}="{value}"' in html)
        
        # Check that the content is correctly nested
        self.assertTrue("<p>Content</p>" in html)
    
    def test_parent_with_special_characters(self): # Test handling of special characters in content
        parent = ParentNode("div", [
            LeafNode("p", "Special chars: < > & \" '"),
            LeafNode("code", "if (x < 10 && y > 20)")
        ])
        
        html = parent.to_html()
        self.assertTrue("<p>Special chars: < > & \" '</p>" in html)
        self.assertTrue("<code>if (x < 10 && y > 20)</code>" in html)

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
        
if __name__ == "__main__":
    unittest.main()