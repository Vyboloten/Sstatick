import unittest
from src.textnode import TextNode, TextType
from src.main import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Tthis siis is texxt", TextType.ITALIC)
        node2 = TextNode("Tthis siis is texxt", TextType.BOLD)
        self.assertNotEqual (node, node2)
    
    def test_without_url(self):
    # Create a node with no URL (uses default None)
        node_without_url = TextNode("Check this link", TextType.LINK)
    # Create a node with the same text and type, but with a URL
        node_with_url = TextNode("Check this link", TextType.LINK, "https://example.com")
    # They should not be equal since one has a URL and the other doesn't
        self.assertNotEqual(node_without_url, node_with_url)

    def test_different_text(self):
        node = TextNode("Tthis siis is texxt", TextType.ITALIC)
        node2 = TextNode("This is is text", TextType.ITALIC)
        self.assertNotEqual (node, node2)

    def test_different_url(self):
        first_url = TextNode("Check this link", TextType.LINK, "https://test.com")
        second_url = TextNode("Check this link", TextType.LINK, "https://example.com")
        self.assertNotEqual (first_url, second_url)
    
    def test_empty_node(self):
        empty_node = TextNode("", TextType.TEXT)  # Node with empty text
        non_empty_node = TextNode("Some content", TextType.TEXT)
        self.assertNotEqual(empty_node, non_empty_node)
    # Also test that two empty nodes with the same type are equal
        another_empty_node = TextNode("", TextType.TEXT)
        self.assertEqual(empty_node, another_empty_node)

    def test_none_values(self):
    # Test that None is not equal to a TextNode
        node = TextNode("text", TextType.TEXT)
        self.assertNotEqual(node, None)

    def test_equality_properties(self):
        node = TextNode("text", TextType.BOLD)
    # Reflexivity: x == x
        self.assertEqual(node, node)
     # Symmetry: if x == y then y == x
        node2 = TextNode("text", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertEqual(node2, node)

    def test_special_characters(self):
        special_node = TextNode("!@#$%^&*()", TextType.TEXT)
        special_node2 = TextNode("!@#$%^&*()", TextType.TEXT)
        self.assertEqual(special_node, special_node2)

    def test_different_url_protocols(self):
        http_node = TextNode("link", TextType.LINK, "http://example.com")
        https_node = TextNode("link", TextType.LINK, "https://example.com")
        self.assertNotEqual(http_node, https_node)
    
    def test_long_text(self):
        long_text = "a" * 1000  
    # A string of 1000 'a' characters
        long_node1 = TextNode(long_text, TextType.TEXT)
        long_node2 = TextNode(long_text, TextType.TEXT)
        self.assertEqual(long_node1, long_node2)
        
class Test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, {})

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, {})

    def test_code(self):
        node = TextNode("let x = 5;", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "let x = 5;")
        self.assertEqual(html_node.props, {})

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Image should have empty value
        self.assertEqual(html_node.props, {"src": "https://www.example.com/image.png", "alt": "Alt text"})

    def test_invalid_type(self): # Create a TextNode with an invalid type (assuming -1 is not a valid TextType)
        node = TextNode("Invalid type", -1)
        # Assert that calling text_node_to_html_node with this node raises an Exception
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_empty_text(self): #Test that empty text still works correctly
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {})

    def test_special_characters(self): #Test that special characters are preserved
        special_text = "Text with <>&\" special chars"
        node = TextNode(special_text, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, special_text)
        self.assertEqual(html_node.props, {})

    def test_link_no_url(self): #Test a link with no URL (this might be an edge case)
        node = TextNode("Link text", TextType.LINK, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props, {"href": ""})

    def test_image_no_url(self): #Test an image with no URL (this might be an edge case)
        node = TextNode("Alt text", TextType.IMAGE, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "", "alt": "Alt text"})

    def test_multiline_text(self): #Test that multiline text is preserved correctly
        multiline_text = "Line 1\nLine 2\nLine 3"
        node = TextNode(multiline_text, TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, multiline_text)
        self.assertEqual(html_node.props, {})

    def test_unicode_characters(self): #Test that Unicode characters are handled properly
        unicode_text = "こんにちは世界! 👋 🌍"
        node = TextNode(unicode_text, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, unicode_text)
        self.assertEqual(html_node.props, {})

    def test_long_text(self): #Test with a long text string
        long_text = "a" * 1000  # A string with 1000 'a' characters
        node = TextNode(long_text, TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, long_text)
        self.assertEqual(html_node.props, {})

    def test_numeric_text(self): #Test with numeric content
        numeric_text = "12345"
        node = TextNode(numeric_text, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, numeric_text)
        self.assertEqual(html_node.props, {})

    def test_complex_url(self): #Test with a complex URL containing query parameters and fragments
        complex_url = "https://example.com/path?param1=value1&param2=value2#fragment"
        node = TextNode("Complex URL", TextType.LINK, complex_url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Complex URL")
        self.assertEqual(html_node.props, {"href": complex_url})

    def test_image_with_complex_url(self): #Test an image with a complex URL
        complex_url = "https://example.com/images/photo.jpg?width=800&height=600"
        node = TextNode("Image description", TextType.IMAGE, complex_url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": complex_url, "alt": "Image description"})

    def test_conversion_preserves_original(self): #Test that converting to HTML doesn't modify the original TextNode
        original_text = "Original Text"
        original_url = "https://example.com"
        node = TextNode(original_text, TextType.LINK, original_url)
        
        # Convert to HTML
        html_node = text_node_to_html_node(node)
        
        # Verify original TextNode is unchanged
        self.assertEqual(node.text, original_text)
        self.assertEqual(node.url, original_url)
        self.assertEqual(node.text_type, TextType.LINK)

    def test_nested_html_in_text(self): #Test handling text that contains HTML-like content
        html_text = "<p>This looks like HTML but should be treated as text</p>"
        node = TextNode(html_text, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, html_text)
        self.assertEqual(html_node.props, {})

    def test_zero_length_text(self): #Test with zero-length text for all types
        for text_type in [TextType.TEXT, TextType.BOLD, TextType.ITALIC, TextType.CODE]:
            node = TextNode("", text_type)
            html_node = text_node_to_html_node(node)
            if text_type == TextType.TEXT:
                self.assertEqual(html_node.tag, None)
            elif text_type == TextType.BOLD:
                self.assertEqual(html_node.tag, "b")
            elif text_type == TextType.ITALIC:
                self.assertEqual(html_node.tag, "i")
            elif text_type == TextType.CODE:
                self.assertEqual(html_node.tag, "code")
            self.assertEqual(html_node.value, "")

    def test_whitespace_only(self): #Test with whitespace-only text
        whitespace = "   \t\n  "
        node = TextNode(whitespace, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, whitespace)

    def test_link_with_special_characters_in_url(self): #Test links with special characters in the URL
        url_with_special = "https://example.com/search?q=special chars+%20@#$"
        node = TextNode("Special URL", TextType.LINK, url_with_special)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Special URL")
        self.assertEqual(html_node.props, {"href": url_with_special})

    def test_image_alt_with_quotes(self): #Test image with quotes in alt text
        alt_with_quotes = 'Image with "quotes" inside'
        node = TextNode(alt_with_quotes, TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": alt_with_quotes})
        
    def test_multiple_conversions(self): #Test that multiple conversions work properly
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Link text", TextType.LINK, "https://example.com")
        ]
        
        html_nodes = [text_node_to_html_node(node) for node in nodes]
        
        # Check first node
        self.assertEqual(html_nodes[0].tag, None)
        self.assertEqual(html_nodes[0].value, "Regular text")
        self.assertEqual(html_nodes[0].props, {})
        
        # Check second node
        self.assertEqual(html_nodes[1].tag, "b")
        self.assertEqual(html_nodes[1].value, "Bold text")
        self.assertEqual(html_nodes[1].props, {})
        
        # Check third node
        self.assertEqual(html_nodes[2].tag, "a")
        self.assertEqual(html_nodes[2].value, "Link text")
        self.assertEqual(html_nodes[2].props, {"href": "https://example.com"})

    def test_invalid_text_type(self): #Test that an invalid text type raises an exception
        # Create a TextNode with an invalid text type (assuming 999 is not a valid TextType)
        # This requires modifying the TextNode to allow this invalid state for testing
        # Alternatively, you could use mock to simulate this scenario
        class FakeTextType:
            def __init__(self, value):
                self.value = value
                
        invalid_node = TextNode("Invalid type", FakeTextType(999))
        
        # The function should raise an exception
        with self.assertRaises(Exception):
            text_node_to_html_node(invalid_node)

    def test_none_text(self): #Test that None text is handled properly
        # Using None as text is likely an edge case that should be handled
        node = TextNode(None, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, None)  # Or perhaps "" if your implementation converts None to empty string

    def test_none_url(self): #Test that None URL for links and images is handled properly
        # Link with None URL
        link_node = TextNode("Link text", TextType.LINK, None)
        link_html = text_node_to_html_node(link_node)
        self.assertEqual(link_html.tag, "a")
        self.assertEqual(link_html.value, "Link text")
        self.assertEqual(link_html.props, {"href": None})  # Or "" if your implementation converts None to empty string
        
        # Image with None URL
        img_node = TextNode("Alt text", TextType.IMAGE, None)
        img_html = text_node_to_html_node(img_node)
        self.assertEqual(img_html.tag, "img")
        self.assertEqual(img_html.value, "")
        self.assertEqual(img_html.props, {"src": None, "alt": "Alt text"})  # Or "" if your implementation converts None to empty string

    def test_code_with_special_syntax(self): #Test code blocks with programming syntax
        code_text = "def hello_world():\n    print('Hello, World!')"
        node = TextNode(code_text, TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, code_text)
        self.assertEqual(html_node.props, {})
    
    def test_image_with_empty_alt(self): #Test image with empty alt text
        node = TextNode("", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": ""})

    def test_html_entities_in_text(self): #Test with text containing HTML entities
        entity_text = "Less than < and greater than > symbols & ampersand"
        node = TextNode(entity_text, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, entity_text)
        self.assertEqual(html_node.props, {})
        
if __name__ == "__main__":
    unittest.main()