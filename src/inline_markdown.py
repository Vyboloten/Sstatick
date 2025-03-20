import re
from src.textnode import TextNode, TextType

def extract_markdown_images(text):
    # Matches valid Markdown images
    #pattern = r"(?:^|\s)!\[([^\[\]\n]+)\]\((https?://[^\s\(\)]+\.[^\s\(\)]+)\)(?=\s|$)"
    #pattern = r'!\[([^\[\]\n]*)\]\((https?://[^\s\(\)]+(?:\.[a-zA-Z]{2,})(?:[^\s\(\)]*)?)\)'
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    #pattern = r"!\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)"
    matches = re.findall(pattern, text)
    valid_matches = []
    for match in matches:
        if not match[0] or not match[1]:  # Check alt text and URL
            raise ValueError("Malformed image markdown found: missing alt text or URL.")
        valid_matches.append(match)
    return matches

def extract_markdown_links(text):
    #pattern = r"\[([^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*?)\]\((https?://[^\s\)]+)\)"
    #pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    #pattern = r"(?<!!)\[((?:\\.|[^\[\]])*)\]\(((?:\\.|[^\(\)])*)\)"
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    valid_matches = []
    for match in matches:
        if not match[0] or not match[1]:  # Check if either alt text or URL is missing
            raise ValueError("Malformed link markdown found: missing alt text or URL.")
        valid_matches.append(match)
    
    return valid_matches


def split_nodes_delimiter(old_nodes, delimiter, text_type):

        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("Invalid markdown: formatted section not closed.")
            
            split_nodes = []
            for i, section in enumerate(sections):
                if section:
                    node_type = TextType.TEXT if i % 2 == 0 else text_type
                    split_nodes.append(TextNode(section, node_type))
                    
            new_nodes.extend(split_nodes)
        return new_nodes

def split_nodes_image(old_nodes):
    """
    Split TextNodes that contain image markdown into separate TextNodes.
    Args: old_nodes: A list of TextNode objects
    Returns: A list of TextNode objects where any images have been extracted into their own nodes
    
    new_nodes = []
    # Process each node in the input list
    for old_node in old_nodes:
        # Skip nodes that aren't of type TEXT (we only process plain text nodes)
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue  
        # Extract all image information using your extract_images function
        images = extract_markdown_images(old_node.text)
        # If no images found, just add the original node and continue
        if not images:
            new_nodes.append(old_node)
            continue
        # If we found images, we need to split the text
        remaining_text = old_node.text
        # Process each image
        for image_alt, image_url in images:
            # Find the image markdown pattern in the text
            image_markdown = f"![{image_alt}]({image_url})"
            # Split the text at the image markdown (only split once)
            parts = remaining_text.split(image_markdown, 1)
            # Add the text before the image as a TEXT node (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            # Add the image as an IMAGE node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            # Update remaining text to be the part after the image
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        # Add any remaining text after the last image (if not empty)
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes"""
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            parts = remaining_text.split(link_markdown, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes   """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if not links:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            
            # Add text section before the link, including leading/trailing whitespace
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add the link node
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            
            # Update original_text for the remaining part after the link
            original_text = sections[1]
        
        # Add remaining text after the last link, including leading/trailing whitespace
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    ###print(f"Processing text: {text}")
    # Step 1: Validate input (to catch improper types, as we discussed)
    if not isinstance(text, str):
        raise TypeError(f"Expected string input, got {type(text)} instead.")

    # Step 2: Start with a single text node
    nodes = [TextNode(text, TextType.TEXT)]

    # Step 3: Process bold, italic, and code using existing functions
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    #nodes = [node for node in nodes if node.text != ""]
    ###print(f"Generated text nodes: {nodes}")
    return nodes

"""def ensure_valid_nodes(nodes):
    for idx, node in enumerate(nodes):
        print(f"Node {idx}: {node}, type: {type(node)}")
        if not isinstance(node, TextNode):
            print(f"Invalid node found at index {idx}: {node}")
    assert all(isinstance(node, TextNode) for node in nodes), "Nodes list contains invalid items!"
"""

def markdown_to_blocks(markdown):
    # Strip global whitespace/newlines on the input Markdown string
    markdown = markdown.strip()
    # Split by double newlines into blocks
    blocks = markdown.split('\n\n')
    new_blocks = []
    for block in blocks:
        # Clean lines individually inside the block
        cleaned_lines = [line.strip() for line in block.splitlines()]
        # Rejoin cleaned lines and then strip the entire block
        cleaned_block = '\n'.join(cleaned_lines).strip()
        # Add cleaned block only if it's not empty
        if cleaned_block:
            new_blocks.append(cleaned_block)
    return new_blocks
# Split the markdown into blocks divided by two newline characters
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        # Clean each line inside the block to handle inconsistent indentation
        lines = block.splitlines()
        cleaned_lines = [line.strip() for line in lines]  # Strip each line
        reconstructed_block = "\n".join(cleaned_lines)  # Rejoin cleaned lines
        # Add the cleaned block only if it's not empty
        filtered_blocks.append(reconstructed_block)
    return filtered_blocks
