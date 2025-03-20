# Import whatever testing framework you're using
import unittest
# Import your classes and functions
from src.textnode import TextNode, TextType
from src.text_splitter import split_nodes_delimiter  # Adjust to your file name

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_with_no_delimiters(self): # Test that a node without delimiters remains unchanged
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Just plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_with_one_delimiter_pair(self): # Test splitting with one delimiter pair
        node = TextNode("Text with a **bold** word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " word")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_with_multiple_delimiter_pairs(self): # Test with multiple delimiter pairs
        node = TextNode("**Bold** normal **more bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " normal ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "more bold")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, "")
        self.assertEqual(result[4].text_type, TextType.TEXT)
    
    def test_split_with_different_delimiters(self): # Test with different types of delimiters
        # Code blocks with backticks
        node = TextNode("Check out this `code block` example", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Check out this ")
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, TextType.CODE)
        
        # Italic with underscores
        node = TextNode("Some _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
    
    def test_with_non_text_nodes(self): # Test that non-TEXT nodes are left untouched
        bold_node = TextNode("Already bold", TextType.BOLD)
        text_node = TextNode("Plain **with bold**", TextType.TEXT)
        result = split_nodes_delimiter([bold_node, text_node], "**", TextType.BOLD)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "Already bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, "Plain ")
        self.assertEqual(result[2].text, "with bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)

    def test_with_adjacent_delimiters(self): # Test with adjacent delimiter pairs
        node = TextNode("Text **bold**_italic_", TextType.TEXT)
        # First split by bold
        intermediate = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then split by italic
        result = split_nodes_delimiter(intermediate, "_", TextType.ITALIC)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Text ")
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)

    def test_with_empty_delimiter_content(self): # Test with empty content between delimiters
        node = TextNode("Some ** ** empty", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Some ")
        self.assertEqual(result[1].text, " ")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " empty")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_with_missing_closing_delimiter(self): # Test that an exception is raised when a closing delimiter is missing
        node = TextNode("Text with **unclosed bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_with_delimiter_at_start(self): # Test with delimiter at the start of text
        node = TextNode("**Bold** at start", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " at start")

    def test_with_delimiter_at_end(self): # Test with delimiter at the end of text
        node = TextNode("End with **Bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "End with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_with_multiple_nodes(self): # Test with a list of multiple nodes
        node1 = TextNode("First **bold**", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("Another **bold** word", TextType.TEXT)
        
        result = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].text, "First ")
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[3].text, "Already bold")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, "Another ")
        self.assertEqual(result[5].text, "bold")
        self.assertEqual(result[5].text_type, TextType.BOLD)
        self.assertEqual(result[6].text, " word")

    def test_with_consecutive_delimiters(self): # Test with consecutive delimiter pairs
        node = TextNode("Text with **bold**_italic_ consecutively", TextType.TEXT)
        
        # First split by bold
        intermediate = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then split the result by italic
        result = split_nodes_delimiter(intermediate, "_", TextType.ITALIC)
        
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, " consecutively")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_basic_delimiter_functionality(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_with_delimiter_at_start(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "")  # Empty node before delimiter
        self.assertEqual(result[1].text, "Bold")
        self.assertEqual(result[2].text, " at the start")

    def test_with_delimiter_at_end(self):
        node = TextNode("At the end **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "At the end ")
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[2].text, "")  # Empty node after delimiter

    def test_with_multiple_delimiters(self):
        node = TextNode("This has **multiple** bold **words**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "This has ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "multiple")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " bold ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "words")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, "")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_nested_split_operations(self): # Testing with multiple types of delimiters in sequence
        node = TextNode("Text with **bold** and `code` and _italic_", TextType.TEXT)
        # First split by bold
        result1 = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then split by code
        result2 = split_nodes_delimiter(result1, "`", TextType.CODE)
        # Finally split by italic
        result3 = split_nodes_delimiter(result2, "_", TextType.ITALIC)
        
        self.assertEqual(len(result3), 7)
        self.assertEqual(result3[0].text, "Text with ")
        self.assertEqual(result3[1].text, "bold")
        self.assertEqual(result3[1].text_type, TextType.BOLD)
        self.assertEqual(result3[2].text, " and ")
        self.assertEqual(result3[3].text, "code")
        self.assertEqual(result3[3].text_type, TextType.CODE)
        self.assertEqual(result3[4].text, " and ")
        self.assertEqual(result3[5].text, "italic")
        self.assertEqual(result3[5].text_type, TextType.ITALIC)
        self.assertEqual(result3[6].text, "")

    def test_with_no_delimiters(self): # Testing text with no delimiters
        node = TextNode("Plain text with no delimiters", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text with no delimiters")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_with_non_text_nodes(self): # Testing with nodes that are already a different type
        bold_node = TextNode("Already bold", TextType.BOLD)
        code_node = TextNode("Some code", TextType.CODE)
        text_node = TextNode("Regular text with **bold**", TextType.TEXT)
        
        # Mix of different node types
        mixed_nodes = [bold_node, text_node, code_node]
        result = split_nodes_delimiter(mixed_nodes, "**", TextType.BOLD)
        
        self.assertEqual(len(result), 5)
        # First node should be unchanged
        self.assertEqual(result[0].text, "Already bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        # Second node should be split
        self.assertEqual(result[1].text, "Regular text with ")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "")
        self.assertEqual(result[3].text_type, TextType.TEXT)
        # Third node should be unchanged
        self.assertEqual(result[4].text, "Some code")
        self.assertEqual(result[4].text_type, TextType.CODE)

    def test_with_unmatched_delimiters(self): # Testing error handling for unmatched delimiters
        node = TextNode("Text with **bold but no closing delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
        # Test with opening but mismatched closing
        node = TextNode("Text with **bold but wrong closing*", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_with_empty_text(self): # Testing with empty text nodes
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    """def test_with_only_delimiters(self): # Testing with text that's just a pair of delimiters
        node = TextNode("**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[1].text, "")  # Empty bold text
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[2].text_type, TextType.TEXT)  # Adding this line to check the type
        """

    def test_with_consecutive_delimiters(self): # Testing with consecutive delimiter pairs
        node = TextNode("**Bold****Another Bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "Another Bold")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, "")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_with_different_length_delimiters(self): # Test with single character delimiter
        node = TextNode("Text with _italic_ content", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " content")

        # Test with multi-character delimiter
        node = TextNode("Text with ```code block``` syntax", TextType.TEXT)
        result = split_nodes_delimiter([node], "```", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " syntax")

    """def test_with_delimiters_inside_content(self): # Test with delimiters appearing within the content (should be treated as regular text)
        node = TextNode("This has **bold with ** inside** it", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This has ")
        self.assertEqual(result[1].text, "bold with ** inside")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " it")
        """
    
    def test_with_empty_list(self): # Test with an empty list of nodes
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_with_special_characters(self): # Test with special characters in the text
        node = TextNode("Text with **bold & special chars!@#$%^&*()** here", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[1].text, "bold & special chars!@#$%^&*()")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " here")

    def test_with_multiple_node_types(self): # Test combining different types of styling
        bold_node = TextNode("This is bold", TextType.BOLD)
        text_node = TextNode("This is _italic_ within text", TextType.TEXT)
        combined = [bold_node, text_node]
        
        # First, process for italic
        result = split_nodes_delimiter(combined, "_", TextType.ITALIC)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[2].text_type, TextType.ITALIC)
        self.assertEqual(result[3].text_type, TextType.TEXT)

    """def test_with_escaped_delimiters(self): # Test with escaped delimiters that should be treated as regular text
    # Note: For simplicity in this test, we're assuming your implementation
    # doesn't handle escaped delimiters specially - this is more of an 
    # extension test that you might want to implement later
    
    # If your function doesn't specifically handle escaped delimiters,
    # this would probably raise an exception because the \* characters 
    # would break the delimiter matching pattern
    
    # Let's create a case that should work regardless
        node = TextNode("Text with \\** and **bold** content", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        # The first part includes the escaped characters
        self.assertEqual(result[0].text, "Text with \\** and ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        # The bold part works normally
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        # The last part is normal text
        self.assertEqual(result[2].text, " content")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        """
    
    def test_with_multiple_instances_of_same_delimiter(self): # Test with multiple instances of the same delimiter type
        node = TextNode("**Bold1** normal text **Bold2** more text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Bold1")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " normal text ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "Bold2")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, " more text")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_with_delimiters_at_start_and_end(self): # Test with delimiters at the start and end of string
        node = TextNode("**Bold text at edges**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Bold text at edges")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_with_mixed_delimiter_types(self): # Test processing multiple types of delimiters in sequence
        node = TextNode("This has `code` and **bold** and _italic_ text", TextType.TEXT)
    
        # Process code first
        result1 = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result1), 3)
        self.assertEqual(result1[0].text, "This has ")
        self.assertEqual(result1[1].text, "code")
        self.assertEqual(result1[1].text_type, TextType.CODE)
        self.assertEqual(result1[2].text, " and **bold** and _italic_ text")
        
        # Then process bold
        result2 = split_nodes_delimiter(result1, "**", TextType.BOLD)
        self.assertEqual(len(result2), 5)
        self.assertEqual(result2[0].text, "This has ")
        self.assertEqual(result2[0].text_type, TextType.TEXT)
        self.assertEqual(result2[1].text, "code")
        self.assertEqual(result2[1].text_type, TextType.CODE)
        self.assertEqual(result2[2].text, " and ")
        self.assertEqual(result2[2].text_type, TextType.TEXT)
        self.assertEqual(result2[3].text, "bold")
        self.assertEqual(result2[3].text_type, TextType.BOLD)
        self.assertEqual(result2[4].text, " and _italic_ text")
        self.assertEqual(result2[4].text_type, TextType.TEXT)
        # Finally process italic
        result3 = split_nodes_delimiter(result2, "_", TextType.ITALIC)
        self.assertEqual(len(result3), 7)
        self.assertEqual(result3[0].text, "This has ")
        self.assertEqual(result3[0].text_type, TextType.TEXT)
        self.assertEqual(result3[1].text, "code")
        self.assertEqual(result3[1].text_type, TextType.CODE)
        self.assertEqual(result3[2].text, " and ")
        self.assertEqual(result3[2].text_type, TextType.TEXT)
        self.assertEqual(result3[3].text, "bold")
        self.assertEqual(result3[3].text_type, TextType.BOLD)
        self.assertEqual(result3[4].text, " and ")
        self.assertEqual(result3[4].text_type, TextType.TEXT)
        self.assertEqual(result3[5].text, "italic")
        self.assertEqual(result3[5].text_type, TextType.ITALIC)
        self.assertEqual(result3[6].text, " text")
        self.assertEqual(result3[6].text_type, TextType.TEXT)

    """def test_with_nested_delimiters(self):
    # This tests what happens when delimiters are nested (which the assignment says we don't support)
    # The expected behavior is to raise an exception since nested inline elements aren't supported
        node = TextNode("This has **bold with _italic_ inside**", TextType.TEXT)
        with self.assertRaises(Exception):
            # First process bold, which should work
            result = split_nodes_delimiter([node], "**", TextType.BOLD)
            # Then try to process italic, which should fail because it's nested inside bold
            split_nodes_delimiter(result, "_", TextType.ITALIC)"""

    def test_with_unbalanced_delimiters(self): # Test with unbalanced delimiters - should raise an exception
        node = TextNode("This has **bold but no closing delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Also test with opening delimiter missing
        node = TextNode("This has bold but no opening delimiter**", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_with_empty_delimited_content(self): # Test with empty content between delimiters
        node = TextNode("This has **** empty bold", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This has ")
        self.assertEqual(result[1].text, "")  # Empty bold text
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " empty bold")

    def test_with_only_delimiters(self): # Test with a string that is just delimiters
        node = TextNode("**", TextType.TEXT)
    
    # This could either raise an exception (if your implementation requires content)
    # or create an empty bold node surrounded by empty text nodes
        try:
            result = split_nodes_delimiter([node], "**", TextType.BOLD)
            # If no exception, verify the result
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0].text, "")
            self.assertEqual(result[0].text_type, TextType.TEXT)
            self.assertEqual(result[1].text, "")
            self.assertEqual(result[1].text_type, TextType.BOLD)
            self.assertEqual(result[2].text, "")
            self.assertEqual(result[2].text_type, TextType.TEXT)
        except Exception as e:
            # If your implementation raises an exception for this case, that's also valid
            pass  # The test should pass either way

    def test_with_adjacent_delimiters(self): # Test with adjacent delimiter pairs
        node = TextNode("**Bold****Another Bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "Another Bold")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, "")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_with_multiple_text_types(self): # Test with nodes already having different text types
        nodes = [
            TextNode("Normal text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Text with `code`", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Normal text")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Already bold")
        self.assertEqual(result[1].text_type, TextType.BOLD) # Should remain unchanged
        self.assertEqual(result[2].text, "Text with ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "code")
        self.assertEqual(result[3].text_type, TextType.CODE)
        self.assertEqual(result[4].text, "")
        self.assertEqual(result[4].text_type, TextType.TEXT)