import unittest
from src.blocktype import BlockType, block_to_block_type, markdown_to_html_node
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.blocktype import block_to_html_node
from src.blocktype import text_to_textnodes, text_to_children, markdown_to_blocks
from src.textnode import TextType, TextNode

class TestMarkdownPipeline(unittest.TestCase):
    
    def test_heading(self):
        block = "# Heading 1"
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].value, "Heading 1")
    
    def test_paragraph(self):
        block = "This is **bold** and _italic_ text."
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "p")
        self.assertEqual(len(node.children), 5)  # Text split into nodes for plain, bold, italic
        self.assertEqual(node.children[1].tag, "b")  # Bold
        self.assertEqual(node.children[1].value, "bold")
        self.assertEqual(node.children[3].tag, "i")  # Italic
        self.assertEqual(node.children[3].value, "italic")
    
    """def test_code_block(self):
        block = "```\nCode block content\n```"
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "pre")
        self.assertEqual(len(node.children), 1)
        code_node = node.children[0]
        self.assertEqual(code_node.tag, "code")
        self.assertEqual(len(code_node.children), 1)
        self.assertEqual(code_node.children[0].value, "Code block content")"""
    
    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 3)  # Three list items
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(node.children[0].children[0].value, "Item 1")
        self.assertEqual(node.children[2].children[0].value, "Item 3")
    
    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 3)  # Three list items
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(node.children[0].children[0].value, "First item")
        self.assertEqual(node.children[2].children[0].value, "Third item")
    
    def test_quote(self):
        block = "> This is a quote."
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].value, "This is a quote.")
    
    """def test_unrecognized_block_type(self):
        block = "This shouldn't be recognized"
        node = block_to_html_node(block, None)  # Passing an unrecognized block type
        self.assertIsNone(node)  # Should return None for unrecognized types"""

    """def test_multiline_heading(self):
        block = "# Heading with multiple lines\nand extra text"
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.children[0].value, "Heading with multiple lines and extra text")"""

    """def test_empty_paragraph(self):
        block = ""
        node = block_to_html_node(block)
        self.assertIsNone(node)  # Should return None for empty paragraphs"""

    """def test_code_block_with_empty_lines(self):
        block = "```\n\nCode content with empty lines\n\n```"
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "pre")
        self.assertEqual(node.children[0].tag, "code")
        self.assertEqual(node.children[0].children[0].value, "Code content with empty lines")
    """
    """def test_unordered_list_with_inconsistent_markers(self):
        block = "- Item 1\n* Item 2\n- Item 3"
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].children[0].value, "Item 1")
        self.assertEqual(node.children[1].children[0].value, "Item 2")
        self.assertEqual(node.children[2].children[0].value, "Item 3")"""

    """def test_ordered_list_with_large_numbers(self):
        block = "100. First item\n101. Second item\n102. Third item"
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].children[0].value, "First item")
        self.assertEqual(node.children[2].children[0].value, "Third item")"""

    def test_mixed_content_paragraph(self):
        block = "Text with **bold**, _italic_, and `code`.\nAnd a new line."
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "p")
        self.assertEqual(len(node.children), 7)  # Account for splitting text and formatting nodes
        self.assertEqual(node.children[1].tag, "b")
        self.assertEqual(node.children[1].value, "bold")
        self.assertEqual(node.children[3].tag, "i")
        self.assertEqual(node.children[3].value, "italic")
        self.assertEqual(node.children[5].tag, "code")
        self.assertEqual(node.children[5].value, "code")

    def test_empty_list(self):
        block = "- \n- \n- "
        node = block_to_html_node(block)
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 3)
        for child in node.children:
            self.assertEqual(len(child.children), 0)  # Empty items

    """def test_block_with_invalid_block_type(self):
        block = "This block has an invalid type."
        node = block_to_html_node(block, "InvalidType")  # Pass an invalid block type
        self.assertIsNone(node)"""  # Should gracefully handle unknown types and return None
    
    """def test_nested_unordered_list(self):
        block = "- Item 1\n  - Subitem 1.1\n  - Subitem 1.2\n- Item 2"
        node = block_to_html_node(block)
        print("[TEST DEBUG] Final tree structure:")
        print_tree(node)

        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 2)  # Two top-level items

        # Check the nested list under "Item 1"
        item_1 = node.children[0]  # First <li>
        sublist = item_1.children[1]  # Access nested <ul>, which is the second child
        print(f"[TEST DEBUG] Nested list under 'Item 1': {sublist}")
        self.assertIsNotNone(sublist)
        self.assertEqual(sublist.tag, "ul")
        self.assertEqual(len(sublist.children), 2)

        # Check items within the nested list
        subitem_1_1 = sublist.children[0]  # First <li> in nested <ul>
        self.assertEqual(subitem_1_1.children[0].value, "Subitem 1.1")

        subitem_1_2 = sublist.children[1]  # Second <li> in nested <ul>
        self.assertEqual(subitem_1_2.children[0].value, "Subitem 1.2")"""

    """def test_nested_ordered_list(self):
        block = "1. Item 1\n   1.1. Subitem 1.1\n   1.2. Subitem 1.2\n2. Item 2"
        node = block_to_html_node(block)
        print("[TEST DEBUG] Final tree structure:")
        print_tree(node)

        # Validate root <ol>
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 2)  # Two top-level <li> nodes

        # Validate first <li> (Item 1) and its nested <ol>
        item_1 = node.children[0]  # First <li>
        self.assertEqual(len(item_1.children), 2)  # One for content, one for the nested <ol>

        # Access and validate the nested <ol>
        nested_list = item_1.children[1]  # The second child is the nested <ol>
        self.assertIsNotNone(nested_list)
        self.assertEqual(nested_list.tag, "ol")
        self.assertEqual(len(nested_list.children), 2)  # Two nested <li> nodes

        # Validate nested items
        subitem_1_1 = nested_list.children[0]  # First <li> in nested <ol>
        self.assertEqual(subitem_1_1.children[0].value, "Subitem 1.1")

        subitem_1_2 = nested_list.children[1]  # Second <li> in nested <ol>
        self.assertEqual(subitem_1_2.children[0].value, "Subitem 1.2")

        # Validate second top-level <li> (Item 2)
        item_2 = node.children[1]
        self.assertEqual(len(item_2.children), 1)  # Only contains content
        self.assertEqual(item_2.children[0].value, "Item 2")"""
    def test_heading(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1></div>")

    def test_code_block(self):
        md = "```\nCode block content\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>Code block content</code></pre></div>")

    def test_quote(self):
        md = "> This is a quote."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote.</blockquote></div>")

    def test_unordered_list(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. First item\n2. Second item\n3. Third item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>"
        )

    def test_heading_multiline(self):
        md = "# Heading with multiple lines\nstill heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        # The expected output joins heading lines with a space.
        self.assertEqual(html, "<div><h1>Heading with multiple lines still heading</h1></div>")

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>"
        )

    def test_inline_code(self):
        md = "This paragraph has `inline code` in it."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This paragraph has <code>inline code</code> in it.</p></div>"
        )

    """def test_code_block_with_empty_lines(self):
        md = "```\n\nCode block with empty lines\n\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>Code block with empty lines</code></pre></div>"
        )"""

    def test_multiline_quote(self):
        md = "> This is a multi-line quote.\n> It should be combined."
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Lines are joined with a space.
        self.assertEqual(
            html,
            "<div><blockquote>This is a multi-line quote. It should be combined.</blockquote></div>"
        )
    
    """def test_unordered_list_extra_whitespace(self):
        md = "   -   Item 1   \n   -   Item 2   "
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        )"""

    """def test_ordered_list_with_large_numbers(self):
        md = "100. First item\n101. Second item\n102. Third item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )"""

    """def test_nested_unordered_list(self):
        md = "- Item 1\n  - Subitem 1.1\n  - Subitem 1.2\n- Item 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div><ul>"
            "<li>Item 1<ul><li>Subitem 1.1</li><li>Subitem 1.2</li></ul></li>"
            "<li>Item 2</li>"
            "</ul></div>"
        )
        self.assertEqual(html, expected)"""

    """def test_nested_ordered_list(self):
        md = "1. Item 1\n   1.1. Subitem 1.1\n   1.2. Subitem 1.2\n2. Item 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div><ol>"
            "<li>Item 1<ol><li>Subitem 1.1</li><li>Subitem 1.2</li></ol></li>"
            "<li>Item 2</li>"
            "</ol></div>"
        )
        self.assertEqual(html, expected)"""



def print_tree(node, level=0):
    indent = "  " * level
    if isinstance(node, HTMLNode):
        print(f"{indent}<HTMLNode tag='{node.tag}', children=[")
        for child in node.children:
            print_tree(child, level + 1)
        print(f"{indent}]>")
    elif isinstance(node, LeafNode):
        print(f"{indent}<LeafNode value='{node.value}'>")



if __name__ == "__main__":
    unittest.main()