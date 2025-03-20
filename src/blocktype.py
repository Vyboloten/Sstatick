from enum import Enum
import re
from src.inline_markdown import markdown_to_blocks
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import text_node_to_html_node , TextNode, TextType
from src.inline_markdown import text_to_textnodes


class BlockType (Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    # Split block into lines
    lines = block.split('\n')
    # For headings
    """if block.startswith('#'):
    # Count the number of # characters
        count = 0
        for char in block:
            if char == '#':
                count += 1
            else:
                break
        # Check if it's a valid heading (1-6 # followed by a space)
        if 1 <= count <= 6 and len(block) > count and block[count] == ' ':
            # Make sure the heading text doesn't start with another #
            if not (len(block) > count + 1 and block[count + 1] == '#'):
                # And check for no newlines if needed
                if '\n' not in block:
                    return BlockType.HEADING"""
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # For code blocks
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    # For quote blocks - every line must start with '>'
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    # For unordered lists - every line must start with '- '
    # Empty block is not a list
    if not block:
        return BlockType.PARAGRAPH
    
    #if not all(line.startswith('- ') for line in block.split('\n')):
     #   if any(line.startswith('- ') for line in block.split('\n')):
      #      print(f"Debug - empty_items: '{block}'")
    # For unordered lists, every line should either:
    # 1. Be empty (just whitespace)
    # 2. Start with "- " after stripping leading whitespace
    """all_valid_list_lines = True
    has_list_item = False

    for line in lines:
        print(f"Processing line: '{line.strip()}'")
        if not line.strip():  # Empty line
            continue
        if line.startswith('- '):  # Allow single dash or dash with a space as valid
            has_list_item = True
        elif line.strip().startswith('- '):
            has_list_item = True
        else:
            all_valid_list_lines = False
            break

    if all_valid_list_lines and has_list_item:
        return BlockType.UNORDERED_LIST
    # For ordered lists - numbers must start at 1 and increment by 1
    is_ordered_list = True
    expected_number = 1
    for line in lines:
        # Check if line starts with the expected number, a period, and a space
        if not line.startswith(f"{expected_number}. "):
            is_ordered_list = False
            break
        expected_number += 1

    if is_ordered_list:
        return BlockType.ORDERED_LIST"""
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    # Default to paragraph

def markdown_to_html_node(markdown, debug=False):
    """blocks = markdown_to_blocks(markdown)
    print(f"Blocks: {blocks}")
    if debug:
        print(f"Blocks: {blocks}")
    parent = HTMLNode("div", None, [], None)
    for block in blocks:
        block_type = block_to_block_type(block)
        print(f"Block Type: {block_to_block_type(block)}")
        if debug:
            print(f"Processing Block: {block}\nDetected Block Type: {block_type}")
        block_node = block_to_html_node(block, block_type)
        print(f"Generated Block Node: {block_node}")
        if debug:
            print(f"Generated Block Node: {block_node}")
        parent.children.append(block_node)
    if debug:
        print(f"Final Parent Node: {parent}")
    return parent"""
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        """# Heading processing logic
        normalized_block = block.replace("\n", " ").strip()
        level = block.count("#", 0, block.find(" "))  # Count # at start
        content = normalized_block[level:].strip()
        if level < 1 or level > 6 or not content:
            print("Invalid heading block!")
            return None
        node = HTMLNode(f"h{level}", None, [LeafNode(None, content)], None)
        return node"""
        level = 0
        for char in block:
            if char == '#':
                level += 1
            else:
                break
        # Ensure a space follows the '#' pattern.
        if len(block) <= level or block[level] != ' ':
            return None
        # Extract heading text and join multiline strings with a space.
        text = block[level + 1 :].strip()
        text = " ".join(text.splitlines())  # This joins the lines with a space.
        if not text:
            return None
        children = text_to_children(text)
        return ParentNode(f"h{level}", children, None)


    elif block_type == BlockType.PARAGRAPH:
        """# Paragraph processing logic
        children = text_to_children(block)
        if children:
            return HTMLNode("p", None, children, None)"""
        lines = block.split("\n")
        paragraph = " ".join(lines)
        children = text_to_children(paragraph)
        return ParentNode("p", children)

    elif block_type == BlockType.CODE:
        """# Code block processing logic
        lines = block.splitlines()
        content = "\n".join(lines[1:-1]).strip()
        if content:
            code_node = HTMLNode("code", None, [LeafNode(None, content)], None)
            return HTMLNode("pre", None, [code_node], None)"""
        """if not block.startswith("```") or not block.endswith("```"):
            raise ValueError("invalid code block")
        text = block[4:-3].rstrip("\n")"""
        #print("DEBUG: Original block:", repr(block))
        pattern = re.compile(r"^```(?:\s*\w+)?\n(.*?)\n```$", re.DOTALL)
        match = pattern.match(block)
        if not match:
        #    print("DEBUG: Regex did not match the block!")
        #    print("DEBUG: Block representation:", repr(block))
            raise ValueError("invalid code block")
        text = match.group(1).strip()
        #print("DEBUG: Final text after strip:", repr(text))
        raw_text_node = TextNode(text, TextType.TEXT)
        child = text_node_to_html_node(raw_text_node)
        code = ParentNode("code", [child])
        return ParentNode("pre", [code])

    elif block_type == BlockType.QUOTE:
        """# Quote block processing logic
        content = block[1:].strip()  # Strip the initial '>'
        if content:
            return HTMLNode("blockquote", None, [LeafNode(None, content)], None)"""
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("invalid quote block")
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode("blockquote", children)

        """elif block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
        # Determine the list tag
        list_tag = "ul" if block_type == BlockType.UNORDERED_LIST else "ol"

        # Create the root list node
        root_list_node = HTMLNode(list_tag, None, [], None)
        print(f"[DEBUG] Created root list node: {root_list_node}")

        # Stack to manage current lists and indentation levels
        list_stack = [(0, root_list_node)]  # (indentation level, list node)

        # Split the block into individual items
        items = block.strip().split("\n")
        for item in items:
            # Determine the indentation level
            stripped_item = item.lstrip()
            indentation = len(item) - len(stripped_item)
            print(f"[DEBUG] Processing item: '{item}', Indentation: {indentation}")

            # Extract content and create the `<li>` node
            item_content = stripped_item.lstrip("-*0123456789. ").strip()
            print(f"[DEBUG] Extracted item content: '{item_content}'")
            li_node = HTMLNode("li", None, text_to_children(item_content), None)
            print(f"[DEBUG] Created `<li>` node: {li_node}")

            # Adjust stack based on indentation
            print(f"[DEBUG] Current stack (before popping): {list_stack}")
            while list_stack and list_stack[-1][0] > indentation:
                popped = list_stack.pop()
                print(f"[DEBUG] Popped from stack: {popped}")

            # Handle nested lists (if indentation increases)
            if list_stack and list_stack[-1][0] < indentation:
                nested_list_node = HTMLNode(list_tag, None, [], None)
                parent_list = list_stack[-1][1]
                if parent_list.children:
                    last_li = parent_list.children[-1]
                    if not last_li.children:
                        last_li.children = []
                    last_li.children.append(nested_list_node)
                    print(f"[DEBUG] Appended nested list node to parent `<li>`: {last_li}")
                list_stack.append((indentation, nested_list_node))
                print(f"[DEBUG] Pushed nested list onto stack: {nested_list_node}")

            # Append the `<li>` node to the current list level
            print(f"[DEBUG] Current stack (before appending `<li>`): {list_stack}")
            list_stack[-1][1].children.append(li_node)
            print(f"[DEBUG] Appended `<li>` to current list: {list_stack[-1][1]}")"""
    
    elif block_type == BlockType.UNORDERED_LIST:
        items = block.split("\n")
        html_items = []
        for item in items:
            text = item[2:]
            children = text_to_children(text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ul", html_items)

    elif block_type == BlockType.ORDERED_LIST:
        items = block.split("\n")
        html_items = []
        for item in items:
            text = item[3:]
            children = text_to_children(text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ol", html_items)
        #print(f"[DEBUG] Final root list node: {root_list_node}")
    raise ValueError("invalid block type")

def markdown_to_html_node(markdown, debug=False):
    """blocks = markdown_to_blocks(markdown)
    print(f"Blocks: {blocks}")
    if debug:
        print(f"Blocks: {blocks}")
    parent = HTMLNode("div", None, [], None)
    for block in blocks:
        block_type = block_to_block_type(block)
        print(f"Block Type: {block_to_block_type(block)}")
        if debug:
            print(f"Processing Block: {block}\nDetected Block Type: {block_type}")
        block_node = block_to_html_node(block, block_type)
        print(f"Generated Block Node: {block_node}")
        if debug:
            print(f"Generated Block Node: {block_node}")
        parent.children.append(block_node)
    if debug:
        print(f"Final Parent Node: {parent}")
    return parent"""
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        """# Heading processing logic
        normalized_block = block.replace("\n", " ").strip()
        level = block.count("#", 0, block.find(" "))  # Count # at start
        content = normalized_block[level:].strip()
        if level < 1 or level > 6 or not content:
            print("Invalid heading block!")
            return None
        node = HTMLNode(f"h{level}", None, [LeafNode(None, content)], None)
        return node"""
        level = 0
        for char in block:
            if char == '#':
                level += 1
            else:
                break
        # Ensure a space follows the '#' pattern.
        if len(block) <= level or block[level] != ' ':
            return None
        # Extract heading text and join multiline strings with a space.
        text = block[level + 1 :].strip()
        text = " ".join(text.splitlines())  # This joins the lines with a space.
        if not text:
            return None
        children = text_to_children(text)
        return ParentNode(f"h{level}", children, None)


    elif block_type == BlockType.PARAGRAPH:
        """# Paragraph processing logic
        children = text_to_children(block)
        if children:
            return HTMLNode("p", None, children, None)"""
        lines = block.split("\n")
        paragraph = " ".join(lines)
        children = text_to_children(paragraph)
        return ParentNode("p", children)

    elif block_type == BlockType.CODE:
        """# Code block processing logic
        lines = block.splitlines()
        content = "\n".join(lines[1:-1]).strip()
        if content:
            code_node = HTMLNode("code", None, [LeafNode(None, content)], None)
            return HTMLNode("pre", None, [code_node], None)"""
        """if not block.startswith("```") or not block.endswith("```"):
            raise ValueError("invalid code block")
        text = block[4:-3].rstrip("\n")"""
        #print("DEBUG: Original block:", repr(block))
        pattern = re.compile(r"^```(?:\s*\w+)?\r?\n(.*?)\r?\n```$", re.DOTALL)
        match = pattern.match(block)
        if not match:
        #    print("DEBUG: Regex did not match the block!")
        #    print("DEBUG: Block representation:", repr(block))
            raise ValueError("invalid code block")
        text = match.group(1).strip()
        #print("DEBUG: Final text after strip:", repr(text))
        raw_text_node = TextNode(text, TextType.TEXT)
        child = text_node_to_html_node(raw_text_node)
        code = ParentNode("code", [child])
        return ParentNode("pre", [code])

    elif block_type == BlockType.QUOTE:
        """# Quote block processing logic
        content = block[1:].strip()  # Strip the initial '>'
        if content:
            return HTMLNode("blockquote", None, [LeafNode(None, content)], None)"""
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("invalid quote block")
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode("blockquote", children)

        """elif block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
        # Determine the list tag
        list_tag = "ul" if block_type == BlockType.UNORDERED_LIST else "ol"

        # Create the root list node
        root_list_node = HTMLNode(list_tag, None, [], None)
        print(f"[DEBUG] Created root list node: {root_list_node}")

        # Stack to manage current lists and indentation levels
        list_stack = [(0, root_list_node)]  # (indentation level, list node)

        # Split the block into individual items
        items = block.strip().split("\n")
        for item in items:
            # Determine the indentation level
            stripped_item = item.lstrip()
            indentation = len(item) - len(stripped_item)
            print(f"[DEBUG] Processing item: '{item}', Indentation: {indentation}")

            # Extract content and create the `<li>` node
            item_content = stripped_item.lstrip("-*0123456789. ").strip()
            print(f"[DEBUG] Extracted item content: '{item_content}'")
            li_node = HTMLNode("li", None, text_to_children(item_content), None)
            print(f"[DEBUG] Created `<li>` node: {li_node}")

            # Adjust stack based on indentation
            print(f"[DEBUG] Current stack (before popping): {list_stack}")
            while list_stack and list_stack[-1][0] > indentation:
                popped = list_stack.pop()
                print(f"[DEBUG] Popped from stack: {popped}")

            # Handle nested lists (if indentation increases)
            if list_stack and list_stack[-1][0] < indentation:
                nested_list_node = HTMLNode(list_tag, None, [], None)
                parent_list = list_stack[-1][1]
                if parent_list.children:
                    last_li = parent_list.children[-1]
                    if not last_li.children:
                        last_li.children = []
                    last_li.children.append(nested_list_node)
                    print(f"[DEBUG] Appended nested list node to parent `<li>`: {last_li}")
                list_stack.append((indentation, nested_list_node))
                print(f"[DEBUG] Pushed nested list onto stack: {nested_list_node}")

            # Append the `<li>` node to the current list level
            print(f"[DEBUG] Current stack (before appending `<li>`): {list_stack}")
            list_stack[-1][1].children.append(li_node)
            print(f"[DEBUG] Appended `<li>` to current list: {list_stack[-1][1]}")"""
    
    elif block_type == BlockType.UNORDERED_LIST:
        items = block.split("\n")
        html_items = []
        for item in items:
            text = item[2:]
            children = text_to_children(text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ul", html_items)

    elif block_type == BlockType.ORDERED_LIST:
        items = block.split("\n")
        html_items = []
        for item in items:
            text = item[3:]
            children = text_to_children(text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ol", html_items)
        #print(f"[DEBUG] Final root list node: {root_list_node}")
    raise ValueError("invalid block type")


def text_to_children(text):
    """print(f"Processing text to children: {text}")
    text_nodes = text_to_textnodes(text)
    print(f"Generated text nodes: {text_nodes}")

    html_nodes = [text_node_to_html_node(node) for node in text_nodes if node is not None]
    print(f"Generated HTML nodes: {html_nodes}")
    return html_nodes"""
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

