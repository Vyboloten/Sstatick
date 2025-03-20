import unittest
from src.inline_markdown import extract_markdown_images, extract_markdown_links
from src.inline_markdown import split_nodes_image, split_nodes_link
from src.inline_markdown import text_to_textnodes, markdown_to_blocks 
from src.textnode import TextNode, TextType


class Test_extract_markdown_images(unittest.TestCase):
    def test_extract_markdown_images(self):
        # Single valid image
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        # Multiple valid images
        matches = extract_markdown_images(
            "Here is one ![img1](https://example.com/1.png) and another ![img2](https://example.com/2.png)"
        )
        self.assertListEqual(
            [("img1", "https://example.com/1.png"), ("img2", "https://example.com/2.png")],
            matches
        )

    def test_no_images(self):
        # No valid images in the text
        matches = extract_markdown_images(
            "There are no images here, just plain text."
        )
        self.assertListEqual([], matches)

    def test_malformed_image_tags(self):
        matches = extract_markdown_images(
            "Invalid image syntax: ![missing parentheses](https://example.com/missing) and ![broken"
        )
        # Assert that only the valid image is matched, and malformed input is ignored
        expected = [("missing parentheses", "https://example.com/missing")]
        self.assertListEqual(matches, expected)

    def test_valid_image_tags(self):
        matches = extract_markdown_images(
            "Here's a valid image ![valid](https://example.com/image.png)"
        )
        self.assertListEqual(matches, [("valid", "https://example.com/image.png")])

    def test_multiple_valid_image_tags(self):
        matches = extract_markdown_images(
            "Here are multiple images ![image1](https://example.com/1.png) and ![image2](https://foo.com/image2.jpg)"
        )
        self.assertListEqual(
            matches,
            [
                ("image1", "https://example.com/1.png"),
                ("image2", "https://foo.com/image2.jpg"),
            ],
        )

    def test_partial_tag_with_missing_parenthesis(self):
        matches = extract_markdown_images(
            "This image is broken ![broken alt](https://example.com/missing and should not match."
        )
        self.assertListEqual(matches, [])

    def test_missing_alt_text(self):
        text = "![](http://example.com/image.png)"
        with self.assertRaises(ValueError) as context:
            extract_markdown_images(text)
        self.assertEqual(str(context.exception), "Malformed image markdown found: missing alt text or URL.")

    def test_missing_url(self):
        text = "![alt text]()"
        with self.assertRaises(ValueError) as context:
            extract_markdown_images(text)
        self.assertEqual(str(context.exception), "Malformed image markdown found: missing alt text or URL.")

    def test_complex_text_with_valid_and_invalid_cases(self):
        matches = extract_markdown_images(
            "Valid image: ![image](https://example.com/image.png). Invalid: ![broken](https://example No closing parenthesis."
        )
        # Expect the valid image to be extracted, ignoring malformed ones
        self.assertListEqual(matches, [("image", "https://example.com/image.png")])

class Test_extract_markdown_links(unittest.TestCase):
    def test_single_valid_link(self):
        text = "Here is a link [Boot.dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [("Boot.dev", "https://www.boot.dev")])

    # Test 2: Multiple valid links
    def test_multiple_valid_links(self):
        text = "Links: [Google](https://www.google.com) and [YouTube](https://www.youtube.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [
            ("Google", "https://www.google.com"), 
            ("YouTube", "https://www.youtube.com")
        ])

    # Test 3: Link with no anchor text
    def test_missing_url(self):
        text = "[alt text]()"
        with self.assertRaises(ValueError) as context:
            extract_markdown_links(text)
        self.assertEqual(str(context.exception), "Malformed link markdown found: missing alt text or URL.")
 

    # Test 4: Malformed link
    def test_malformed_link(self):
        text = "Here is a broken link [Boot.dev]"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [])

    # Test 5: No links at all
    def test_no_links_in_text(self):
        text = "No links here!"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [])

    # Test 6: Edge cases
    def test_missing_alt_text(self):
        text = "[](http://example.com)"
        with self.assertRaises(ValueError) as context:
            extract_markdown_links(text)
        self.assertEqual(str(context.exception), "Malformed link markdown found: missing alt text or URL.")

    def test_multiple_links(self):
        text = "Here is [first](https://first.com) and [second](https://second.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [
            ("first", "https://first.com"),
            ("second", "https://second.com"),
        ])

    """def test_empty_anchor_or_url(self):
        text = "Here is a []() and [valid](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [
            ("valid", "https://example.com")
        ])"""

class TestMarkdownParser(unittest.TestCase):
    # Tests for split_nodes_image
    def test_split_nodes_image_basic(self): # Test basic image extraction
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_nodes_image_no_images(self): # Test text without any images
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_only_image(self): # Test text that is only an image
        node = TextNode("![solo image](https://example.com/img.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("solo image", TextType.IMAGE, "https://example.com/img.jpg"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_multiple_nodes(self): # Test with multiple input nodes
        nodes = [
            TextNode("Text before", TextType.TEXT),
            TextNode("![image in middle](https://example.com/middle.jpg)", TextType.TEXT),
            TextNode("Text after", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Text before", TextType.TEXT),
                TextNode("image in middle", TextType.IMAGE, "https://example.com/middle.jpg"),
                TextNode("Text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_non_text_nodes(self): # Test with non-TEXT nodes that should be preserved
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("![image](https://example.com/img.jpg)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Regular text", TextType.TEXT),
                TextNode("Bold text", TextType.BOLD),
                TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_basic(self): # Test basic link extraction
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link_no_links(self): # Test text without any links
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_only_link(self): # Test text that is only a link
        node = TextNode("[solo link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("solo link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_multiple_nodes(self): # Test with multiple input nodes
        nodes = [
            TextNode("Text before", TextType.TEXT),
            TextNode("[link in middle](https://example.com/middle)", TextType.TEXT),
            TextNode("Text after", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Text before", TextType.TEXT),
                TextNode("link in middle", TextType.LINK, "https://example.com/middle"),
                TextNode("Text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_non_text_nodes(self): # Test with non-TEXT nodes that should be preserved
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("[link text](https://example.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Regular text", TextType.TEXT),
                TextNode("Bold text", TextType.BOLD),
                TextNode("link text", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_adjacent_links(self): # Test text with adjacent links
        node = TextNode(
            "[first link](https://first.example.com)[second link](https://second.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first link", TextType.LINK, "https://first.example.com"),
                TextNode("second link", TextType.LINK, "https://second.example.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_empty_text_between_links(self): # Test text with empty text between links
        node = TextNode(
            "Start [first link](https://first.example.com) [second link](https://second.example.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first link", TextType.LINK, "https://first.example.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://second.example.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_with_images(self): # Test text with both links and images (should only process links)
        node = TextNode(
            "This has a [link](https://example.com) and an ![image](https://example.com/img.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and an ![image](https://example.com/img.jpg)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_links(self): # Test text with both links and images (should only process images)
        node = TextNode(
            "This has a [link](https://example.com) and an ![image](https://example.com/img.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This has a [link](https://example.com) and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            ],
            new_nodes,
        )

    def test_edge_cases(self): # Empty nodes list
        self.assertListEqual([], split_nodes_link([]))
        self.assertListEqual([], split_nodes_image([]))
        
        # Node with empty text
        node = TextNode("", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))
        self.assertListEqual([node], split_nodes_image([node]))
        
        # Incomplete markdown syntax
        node_incomplete_link = TextNode("This is [incomplete link", TextType.TEXT)
        self.assertListEqual([node_incomplete_link], split_nodes_link([node_incomplete_link]))
        
        node_incomplete_image = TextNode("This is ![incomplete image", TextType.TEXT)
        self.assertListEqual([node_incomplete_image], split_nodes_image([node_incomplete_image]))





    def test_split_nodes_image_at_start(self):
    # Test image at the start of text
        node = TextNode(
            "![first image](https://example.com/first.jpg) then some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first image", TextType.IMAGE, "https://example.com/first.jpg"),
                TextNode(" then some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_at_end(self):
        # Test image at the end of text
        node = TextNode(
            "Some text and then ![last image](https://example.com/last.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some text and then ", TextType.TEXT),
                TextNode("last image", TextType.IMAGE, "https://example.com/last.jpg"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_at_start(self):
        # Test link at the start of text
        node = TextNode(
            "[first link](https://example.com/first) then some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first link", TextType.LINK, "https://example.com/first"),
                TextNode(" then some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_at_end(self):
    # Test link at the end of text
        node = TextNode(
            "Some text and then [last link](https://example.com/last)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Some text and then ", TextType.TEXT),
                TextNode("last link", TextType.LINK, "https://example.com/last"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_with_formatting_in_text(self):
        # Test link with special characters in text
        node = TextNode(
            "This is a [link with **bold** inside](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link with **bold** inside", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    """def test_split_nodes_image_with_special_chars(self):
        # Test image with special characters in alt text
        node = TextNode(
            "This is an ![image with (parentheses) and [brackets]](https://example.com/special.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image with (parentheses) and [brackets]", TextType.IMAGE, "https://example.com/special.jpg"),
            ],
            new_nodes,
        )"""
        
    def test_split_nodes_complex_mixed_content(self):
    # Test with complex mixed content
        node = TextNode(
            "Start ![img1](https://ex.com/1.jpg) middle [link](https://ex.com) ![img2](https://ex.com/2.jpg) end",
            TextType.TEXT,
        )
        # First split by images
        image_split_nodes = split_nodes_image([node])
        # Then split the resulting nodes by links
        final_nodes = split_nodes_link(image_split_nodes)
        
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://ex.com/1.jpg"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://ex.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://ex.com/2.jpg"),
                TextNode(" end", TextType.TEXT),
            ],
            final_nodes,
        )

    def test_split_nodes_urls_with_special_characters(self):
    # Test URLs with query parameters and special characters
        node = TextNode(
            "Check out [this link](https://example.com/path?param=value&other=123) and ![this image](https://example.com/img.jpg?size=large&format=png)",
            TextType.TEXT,
        )
        
        # Test link splitting
        link_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("this link", TextType.LINK, "https://example.com/path?param=value&other=123"),
                TextNode(" and ![this image](https://example.com/img.jpg?size=large&format=png)", TextType.TEXT),
            ],
            link_nodes,
        )
        
        # Test image splitting
        image_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Check out [this link](https://example.com/path?param=value&other=123) and ", TextType.TEXT),
                TextNode("this image", TextType.IMAGE, "https://example.com/img.jpg?size=large&format=png"),
            ],
            image_nodes,
        )

    """def test_split_nodes_with_escaped_brackets(self):
    # Test with escaped brackets and parentheses in text
        node = TextNode(
            "This has \\[escaped brackets\\] and [link with \\[brackets\\]](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has \\[escaped brackets\\] and ", TextType.TEXT),
                TextNode("link with \\[brackets\\]", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )"""

    def test_multiple_nodes_input(self):
    # Test with multiple nodes as input
        nodes = [
            TextNode("First node with [a link](https://first.com)", TextType.TEXT),
            TextNode("Second node", TextType.TEXT),
            TextNode("Third node with ![an image](https://img.com)", TextType.TEXT),
        ]
        
        # Test link splitting
        link_result = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First node with ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://first.com"),
                TextNode("Second node", TextType.TEXT),
                TextNode("Third node with ![an image](https://img.com)", TextType.TEXT),
            ],
            link_result,
        )
        
        # Test image splitting
        image_result = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First node with [a link](https://first.com)", TextType.TEXT),
                TextNode("Second node", TextType.TEXT),
                TextNode("Third node with ", TextType.TEXT),
                TextNode("an image", TextType.IMAGE, "https://img.com"),
            ],
            image_result,
        )

    def test_non_text_nodes_preserved(self):
    # Test that non-TEXT nodes are preserved as-is
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Text with [a link](https://example.com)", TextType.TEXT),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Text with ![an image](https://image.com)", TextType.TEXT),
        ]
        
        # Test link splitting
        link_result = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Regular text", TextType.TEXT),
                TextNode("Bold text", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://example.com"),
                TextNode("Italic text", TextType.ITALIC),
                TextNode("Text with ![an image](https://image.com)", TextType.TEXT),
            ],
            link_result,
        )
        
        # Test image splitting
        image_result = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Regular text", TextType.TEXT),
                TextNode("Bold text", TextType.BOLD),
                TextNode("Text with [a link](https://example.com)", TextType.TEXT),
                TextNode("Italic text", TextType.ITALIC),
                TextNode("Text with ", TextType.TEXT),
                TextNode("an image", TextType.IMAGE, "https://image.com"),
            ],
            image_result,
        )

class TestTestToTestNodes(unittest.TestCase):
    def test_plain_text(self): # Test with simple text without any markdown
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
    
    def test_bold_text(self): # Test with a bold section
        text = "This has a **bold** word"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This has a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " word")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
    
    def test_italic_text(self): # Test with italic text
        text = "This has an _italic_ word"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This has an ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " word")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_code_text(self): # Test with a code block
        text = "This has a `code block`"
        expected_nodes = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ]
        
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(result_nodes, expected_nodes)
   
    def test_image_text(self): # Test with an image
        text = "This has an ![image](https://example.com/img.jpg)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "This has an ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)

    def test_combined_formats(self): #Test text with multiple markdown formats combined
        text = "Here's **bold** and _italic_ in the same text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "Here's ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " in the same text")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)

    """def test_nested_formats(self): #Test handling of potentially nested formats (should treat them as separate)
        text = "**Bold with _italic_ inside**"
        expected_nodes = [
            TextNode("Bold with ", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode(" inside", TextType.BOLD),
        ]
        
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(result_nodes, expected_nodes)"""
        
    def test_empty_text(self): #Test with empty text
        text = ""
        expected_nodes = []
        
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(result_nodes, expected_nodes)

    def test_mixed_nodes(self): 
        text = "**Bold** _italic_ `code` [link](https://example.com) ![image](https://example.com/img.jpg)"
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
        ]
        
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(result_nodes, expected_nodes)

    def test_consecutive_formats(self): #Test handling of consecutive formatted elements"""
        text = "**Bold**_Italic_`Code`"
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("Code", TextType.CODE),
        ]
        
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(result_nodes, expected_nodes)

    def test_multiple_same_format(self): 
    # Test multiple instances of the same format
        input_text_nodes = [TextNode("**Bold** regular **more bold**", TextType.TEXT)]
        
        # Extract the text field of the first TextNode as input
        input_text = input_text_nodes[0].text  # Extract plain string from TextNode
        
        # Define the expected output
        expected_output = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" regular ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
        ]
        
        # Call your function with the string input
        result = text_to_textnodes(input_text)
        
        # Assert the result matches the expected output
        assert len(result) == len(expected_output), "Node count mismatch"
        for i in range(len(result)):
            assert result[i].text == expected_output[i].text, f"Text mismatch at node {i}"
            assert result[i].text_type == expected_output[i].text_type, f"Type mismatch at node {i}"

    """def test_edge_case_formats(self):
        #Test edge cases with formats
        text = "`**Bold inside code**`"
        nodes = text_to_textnodes(text)
        
        # This should be treated as code, not bold inside code
        self.assertEqual(len(nodes), 3)  # Changed from 2 to 3
        
        # Check for empty node at beginning
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        
        # Check the code node
        self.assertEqual(nodes[1].text, "**Bold inside code**")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        # Check for empty node at end
        self.assertEqual(nodes[2].text, "")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        
        # Test another edge case with empty formatting
        text2 = "**_`[](url)![](img)`_**"
        nodes2 = text_to_textnodes(text2)
        # The exact result might depend on your implementation, but verify basic structure
        self.assertGreater(len(nodes2), 1)
        # At minimum, the last node should be an empty TEXT node
        self.assertEqual(nodes2[-1].text, "")
        self.assertEqual(nodes2[-1].text_type, TextType.TEXT) 
        """

    def test_text_to_textnodes(self):
        # Test with the example from the assignment
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        # Expected result
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        # Call your function
        result = text_to_textnodes(text)
        """print("Actual result:")
        for node in result:
            print(f"TextNode('{node.text}', {node.text_type}, '{node.url if node.url else ''}')")
        # Check that the result matches what's expected"""
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            if expected[i].url:
                self.assertEqual(result[i].url, expected[i].url)
        
class TestBlockSplitter(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        expected_output = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]
        blocks = markdown_to_blocks(md)
        assert blocks == expected_output, f"Expected {expected_output}, but got {blocks}"

    # Edge case: Empty input
    def test_empty_input(self):
        md = """
        
        
        """
        assert markdown_to_blocks(md) == [], "Empty markdown should return an empty list"

    def test_single_block(self):
        # Given a single block of Markdown input
        md = "# This is a heading"

        # Expected output: A list with just that block
        expected_output = ["# This is a heading"]

        # Call the function and compare the result
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected_output, f"Expected {expected_output}, but got {result}")

    def test_empty_input(self): #No Blocks (Empty Input Test)
        md = ""
        expected_output = []
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected_output, f"Expected {expected_output}, but got {result}")

    def test_only_blank_lines(self): #Only Blank Lines
        md = "\n\n   \n\n"
        expected_output = []
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected_output, f"Expected {expected_output}, but got {result}")

    def test_single_block_no_newlines(self): #Single Line Without Newlines
        md = "This is a standalone line"
        expected_output = ["This is a standalone line"]
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected_output, f"Expected {expected_output}, but got {result}")

    def test_multiple_blocks_with_extra_blank_lines(self): #Consecutive Newlines (Multiple Blocks)
        md = """
    This is block one


    This is block two


    This is block three
    """
        expected_output = [
            "This is block one",
            "This is block two",
            "This is block three",
        ]
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected_output, f"Expected {expected_output}, but got {result}")

    def test_multiline_block_with_indentation(self): #Multiline Block with Indentation
        md = """
            This is a block
            with multiple lines
                and inconsistent indentation
        """
        expected_output = [
            "This is a block\nwith multiple lines\nand inconsistent indentation",
        ]
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected_output, f"Expected {expected_output}, but got {result}")

if __name__ == "__main__":
    unittest.main()