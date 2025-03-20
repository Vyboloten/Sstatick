import unittest
from src.blocktype import BlockType, block_to_block_type, markdown_to_html_node
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.blocktype import block_to_html_node

class TestBlockToBlockType(unittest.TestCase):
    
    def test_paragraph(self):
        text = "This is a simple paragraph with no special formatting."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
        
    def test_heading(self):
    # Test all valid heading levels 1-6
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Not a heading - 7 or more # characters
        self.assertEqual(block_to_block_type("####### Too many hashtags"), BlockType.PARAGRAPH)
        
        # Not a heading - no space after #
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        
        # Not a heading - # in the middle of text
        self.assertEqual(block_to_block_type("This has a # in the middle"), BlockType.PARAGRAPH)
        
        # Not a heading - # at the end
        self.assertEqual(block_to_block_type("Ends with #"), BlockType.PARAGRAPH)
        
        # Edge case - just a # and space
        self.assertEqual(block_to_block_type("# "), BlockType.HEADING)
        
    def test_code_block(self):
    # Basic code block
        code = "```\ndef hello():\n    print('Hello world')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        
        # Code block with language specified
        code_with_lang = "```python\ndef hello():\n    print('Hello world')\n```"
        self.assertEqual(block_to_block_type(code_with_lang), BlockType.CODE)
        
        # Code block with backticks inside (shouldn't affect detection)
        nested_backticks = "```\nThis has `inline code` inside\n```"
        self.assertEqual(block_to_block_type(nested_backticks), BlockType.CODE)
        
        # Not a code block - only opening backticks
        self.assertEqual(block_to_block_type("```\nIncomplete code block"), BlockType.PARAGRAPH)
        
        # Not a code block - only closing backticks
        self.assertEqual(block_to_block_type("Incomplete code block\n```"), BlockType.PARAGRAPH)
        
        # Not a code block - backticks not at start/end
        self.assertEqual(block_to_block_type("Text before ```\nCode\n``` text after"), BlockType.PARAGRAPH)
        
        # Empty code block
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)   

    def test_quote(self):
    # Basic quote block
        quote = ">This is a quote"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        
        # Multi-line quote block
        multi_line_quote = ">This is a quote\n>And it continues\n>For multiple lines"
        self.assertEqual(block_to_block_type(multi_line_quote), BlockType.QUOTE)
        
        # Quote with space after >
        quote_with_space = "> This has a space after >"
        self.assertEqual(block_to_block_type(quote_with_space), BlockType.QUOTE)
        
        # Not a quote - second line doesn't start with >
        not_quote_1 = ">This is a partial quote\nThis line is not a quote"
        self.assertEqual(block_to_block_type(not_quote_1), BlockType.PARAGRAPH)
        
        # Not a quote - > in the middle of text
        not_quote_2 = "This has a > in the middle"
        self.assertEqual(block_to_block_type(not_quote_2), BlockType.PARAGRAPH)
        
        # Empty quote lines
        empty_quote = ">\n>\n>"
        self.assertEqual(block_to_block_type(empty_quote), BlockType.QUOTE)
        
        # Quote with nested formatting
        nested_quote = ">This quote has *italic* and **bold** text"
        self.assertEqual(block_to_block_type(nested_quote), BlockType.QUOTE)
            
    def test_unordered_list(self):
    # Basic unordered list
        unordered = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(unordered), BlockType.UNORDERED_LIST)
        
        # Unordered list with nested content
        nested_content = "- Item with *italic*\n- Item with **bold**\n- Item with `code`"
        self.assertEqual(block_to_block_type(nested_content), BlockType.UNORDERED_LIST)
        
        # Not an unordered list - missing space after dash
        no_space = "-Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(no_space), BlockType.PARAGRAPH)
        
        # Not an unordered list - second line doesn't start with "- "
        inconsistent = "- Item 1\nItem 2\n- Item 3"
        self.assertEqual(block_to_block_type(inconsistent), BlockType.PARAGRAPH)
        
        # Not an unordered list - uses different markers
        different_markers = "- Item 1\n* Item 2\n+ Item 3"
        self.assertEqual(block_to_block_type(different_markers), BlockType.PARAGRAPH)
        
        # Empty unordered list items
        empty_items = "- \n- \n- "
        self.assertEqual(block_to_block_type(empty_items), BlockType.UNORDERED_LIST)
        
        # Single item unordered list
        single_item = "- Just one item"
        self.assertEqual(block_to_block_type(single_item), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
    # Basic ordered list
        ordered = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(ordered), BlockType.ORDERED_LIST)
        
        # Ordered list with nested content
        nested_content = "1. Item with *italic*\n2. Item with **bold**\n3. Item with `code`"
        self.assertEqual(block_to_block_type(nested_content), BlockType.ORDERED_LIST)
        
        # Not an ordered list - numbers not starting at 1
        wrong_start = "2. Should start with 1\n3. Then continue"
        self.assertEqual(block_to_block_type(wrong_start), BlockType.PARAGRAPH)
        
        # Not an ordered list - numbers not incrementing by 1
        wrong_increment = "1. First item\n3. Skipped number"
        self.assertEqual(block_to_block_type(wrong_increment), BlockType.PARAGRAPH)
        
        # Not an ordered list - missing space after period
        no_space = "1.First item\n2.Second item"
        self.assertEqual(block_to_block_type(no_space), BlockType.PARAGRAPH)
        
        # Not an ordered list - inconsistent format
        inconsistent = "1. First item\nSecond item\n3. Third item"
        self.assertEqual(block_to_block_type(inconsistent), BlockType.PARAGRAPH)
        
        # Empty ordered list items
        empty_items = "1. \n2. \n3. "
        self.assertEqual(block_to_block_type(empty_items), BlockType.ORDERED_LIST)
        
        # Single item ordered list
        single_item = "1. Just one item"
        self.assertEqual(block_to_block_type(single_item), BlockType.ORDERED_LIST)

        # Long ordered list
        long_list = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth"
        self.assertEqual(block_to_block_type(long_list), BlockType.ORDERED_LIST)

    def test_mixed_types(self):
    # Text that starts like a heading but contains other elements
        heading_like = "# This looks like a heading\nbut it has multiple lines"
        self.assertEqual(block_to_block_type(heading_like), BlockType.PARAGRAPH)
        
        # Text that starts like an unordered list but doesn't continue
        list_like = "- This looks like a list\nbut the second line doesn't follow the pattern"
        self.assertEqual(block_to_block_type(list_like), BlockType.PARAGRAPH)
        
        # Text that has code markers inside but not at start/end
        code_like = "This has ```some code``` in the middle"
        self.assertEqual(block_to_block_type(code_like), BlockType.PARAGRAPH)
        
        # Text that has quote markers inside but not at start of each line
        quote_like = ">This line is a quote\nBut this line isn't\n>And this one is again"
        self.assertEqual(block_to_block_type(quote_like), BlockType.PARAGRAPH)
        
        # Text that has ordered list pattern but doesn't increment correctly
        ordered_like = "1. First item\n1. Also first item?\n3. Third item"
        self.assertEqual(block_to_block_type(ordered_like), BlockType.PARAGRAPH)
        
        # Text with multiple markdown elements mixed together
        mixed_markdown = "This paragraph has *italic*, **bold**, and `code`"
        self.assertEqual(block_to_block_type(mixed_markdown), BlockType.PARAGRAPH)

    def test_edge_cases(self):
    # Empty string
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        
        # Whitespace only
        self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)
        
        # Single character
        self.assertEqual(block_to_block_type("#"), BlockType.PARAGRAPH)  # Not a heading without space
        self.assertEqual(block_to_block_type(">"), BlockType.QUOTE)      # Single quote character is valid
        
        # Almost but not quite valid blocks
        self.assertEqual(block_to_block_type("##No space after hash"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("###### # Too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```\nNo closing backticks"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-No space after dash"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.No space after period"), BlockType.PARAGRAPH)

    def test_complex_blocks(self):
        # Complex code block with internal backticks
        complex_code = "```\nfunction() {\n  let x = `template string`;\n  return x;\n}\n```"
        self.assertEqual(block_to_block_type(complex_code), BlockType.CODE)
        
        # Quote with internal formatting
        complex_quote = "> This is a *quote* with **formatting**\n> And multiple lines\n> With `code` inside"
        self.assertEqual(block_to_block_type(complex_quote), BlockType.QUOTE)
        
        # Ordered list with complex content
        complex_ordered = "1. First item with [link](https://example.com)\n2. Second item with *emphasis*\n3. Third item with `code`"
        self.assertEqual(block_to_block_type(complex_ordered), BlockType.ORDERED_LIST)
        
        # Unordered list with complex content
        complex_unordered = "- Item with **bold**\n- Item with *italic*\n- Item with `code`"
        self.assertEqual(block_to_block_type(complex_unordered), BlockType.UNORDERED_LIST)
        
        # Heading with special characters
        complex_heading = "# Heading with $pecial Ch@racters & symbols!"
        self.assertEqual(block_to_block_type(complex_heading), BlockType.HEADING)
        
        # Paragraph with multiple types of formatting
        complex_paragraph = "This paragraph has **bold**, *italic*, `code`, and [links](https://example.com).\nIt spans multiple lines and has some numbers 123 and symbols !@#."
        self.assertEqual(block_to_block_type(complex_paragraph), BlockType.PARAGRAPH)
        
        # Code block with language specifier
        code_with_language = "```python\ndef hello_world():\n    print('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(code_with_language), BlockType.CODE)
        
        # Quote with nested formatting and multiple paragraphs
        nested_quote = "> This is a quote with **bold** and *italic*\n>\n> This is a second paragraph in the quote"
        self.assertEqual(block_to_block_type(nested_quote), BlockType.QUOTE)
        
        # Lists with nested content
        nested_list = "- Main item 1\n  - Sub item A\n  - Sub item B\n- Main item 2"
        self.assertEqual(block_to_block_type(nested_list), BlockType.UNORDERED_LIST)
        
        # Ordered list with various numbering systems
        mixed_ordered = "1. First\n2. Second\ni. Roman numeral?\nA. Letter?"
        self.assertEqual(block_to_block_type(mixed_ordered), BlockType.PARAGRAPH)
        
        # Block that has markdown-like syntax but doesn't follow the rules
        weird_block = "># This looks like a quote and heading\n```But doesn't close properly"
        self.assertEqual(block_to_block_type(weird_block), BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):
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
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )