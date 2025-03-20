from src.textnode import TextNode, TextType



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextNodes based on the given delimiter.
    
    Args:
        old_nodes: List of TextNode objects
        delimiter: String delimiter to split on (e.g. **, _, `)
        text_type: TextType to assign to the delimited text
        
    Returns:
        A new list of TextNode objects with TEXT nodes split by the delimiter
    """
    """new_nodes = []
    
    for old_node in old_nodes:
        # If not a text node, add it as is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # For text nodes, we need to check for delimiters
        text = old_node.text
        result = []
        
        # Process the text until we've handled all delimiter pairs
        while delimiter in text:
            # Find the first opening delimiter
            start_index = text.find(delimiter)
            
            # Check if there's a closing delimiter
            end_index = text.find(delimiter, start_index + len(delimiter))
            if end_index == -1:
                # No closing delimiter found
                raise Exception(f"Invalid markdown: opening delimiter '{delimiter}' without closing delimiter")
            
            # Text before the delimiter (even if it's empty)
            result.append(TextNode(text[:start_index], TextType.TEXT))
            
            # Text between delimiters (without the delimiters themselves)
            delimited_text = text[start_index + len(delimiter):end_index]
            result.append(TextNode(delimited_text, text_type))
            
            # Update text to be the remainder after the closing delimiter
            text = text[end_index + len(delimiter):]
        
        # Always add remaining text after the last delimiter (even if it's empty)
        result.append(TextNode(text, TextType.TEXT))
            
        # Add all processed nodes to our result
        new_nodes.extend(result)
    
    return new_nodes"""
    """new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        text = old_node.text
        
        # Special case for empty text
        if text == "":
            new_nodes.append(TextNode("", TextType.TEXT))
            continue
            
        parts = []
        start_idx = 0
        
        while start_idx < len(text):
            # Find the next opening delimiter
            open_idx = text.find(delimiter, start_idx)
            
            if open_idx == -1:  # No more delimiters
                # Add remaining text as TEXT type
                if start_idx < len(text):
                    parts.append((text[start_idx:], TextType.TEXT))
                break
            
            # Check if this delimiter is escaped with a backslash
            if open_idx > 0 and text[open_idx - 1] == '\\':
                # Add text up to and including the escaped delimiter
                parts.append((text[start_idx:open_idx + len(delimiter)], TextType.TEXT))
                start_idx = open_idx + len(delimiter)
                continue
                
            if open_idx == -1:  # No more delimiters
                # Add remaining text as TEXT type
                if start_idx < len(text):
                    parts.append((text[start_idx:], TextType.TEXT))
                break
                
            # Add text before the delimiter as TEXT type
            if open_idx > start_idx:
                parts.append((text[start_idx:open_idx], TextType.TEXT))
            else:  # Delimiter is at the start
                parts.append(("", TextType.TEXT))
                            
            # Find the closing delimiter
            close_idx = text.find(delimiter, open_idx + len(delimiter))
            
            if close_idx == -1:  # No closing delimiter
                raise Exception(f"Invalid markdown: opening delimiter '{delimiter}' without closing delimiter")
                
            # Add the text between delimiters with the special type
            between_text = text[open_idx + len(delimiter):close_idx]
            parts.append((between_text, text_type))
            
            # Move the start index to after the closing delimiter
            start_idx = close_idx + len(delimiter)
            
            # If we've reached the end of the text, add an empty TEXT node
            if start_idx == len(text):
                parts.append(("", TextType.TEXT))
        
        # Convert all parts to TextNode objects and add to new_nodes
        for part_text, part_type in parts:
            new_nodes.append(TextNode(part_text, part_type))
            
    return new_nodes"""
    """new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        text = old_node.text
        
        # Find all legitimate delimiter positions
        delimiter_positions = []
        i = 0
        while i < len(text):
            pos = text.find(delimiter, i)
            if pos == -1:
                break
            # Check if it's escaped
            if pos > 0 and text[pos - 1] == '\\':
                i = pos + 1  # Skip this one
                continue
            delimiter_positions.append(pos)
            i = pos + len(delimiter)
        
        # If we don't have an even number of delimiters, that's invalid
        if len(delimiter_positions) % 2 != 0:
            raise Exception(f"Invalid markdown: unmatched delimiter '{delimiter}'")
        
        # Create text nodes based on delimiter positions
        start = 0
        for i in range(0, len(delimiter_positions), 2):
            open_pos = delimiter_positions[i]
            close_pos = delimiter_positions[i + 1]
            # Empty-content delimitors are valid (e.g., "**" for empty bold)
            # so we don't need to check if open_pos + len(delimiter) > close_pos

            # Text before the delimited section
            if open_pos == 0:
                new_nodes.append(TextNode("", TextType.TEXT))
            elif start < open_pos:
                new_nodes.append(TextNode(text[start:open_pos], TextType.TEXT))
            
            # The delimited section - can be empty
            delimited_text = text[open_pos + len(delimiter):close_pos]
            new_nodes.append(TextNode(delimited_text, text_type))
            
            start = close_pos + len(delimiter)
            
            # Always add a text node after a delimited section, even if empty
            start = close_pos + len(delimiter)
            if i + 2 < len(delimiter_positions) and start == delimiter_positions[i+2]:
                new_nodes.append(TextNode("", TextType.TEXT))
        
        # Add any remaining text
        if start < len(text):
            new_nodes.append(TextNode(text[start:], TextType.TEXT))
        elif start == len(text):
            new_nodes.append(TextNode("", TextType.TEXT))
        
    return new_nodes"""
    """new_nodes = []
    
    for old_node in old_nodes:
        # If not a text node, just add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        text = old_node.text
        remaining_text = text
        result = []
        
        # Check if delimiters exist at all
        if delimiter not in remaining_text:
            # No delimiters, just add the original node
            result.append(old_node)
        else:
            while delimiter in remaining_text:
                
                # Check for escaped delimiter
                delimiter_index = remaining_text.find(delimiter)
                
                # If the delimiter is escaped (has a backslash before it)
                if delimiter_index > 0 and remaining_text[delimiter_index - 1] == '\\':
                    # Add text up to the escaped delimiter (including backslash)
                    text_before = remaining_text[:delimiter_index - 1] + remaining_text[delimiter_index:delimiter_index + len(delimiter)]
                    result.append(TextNode(text_before, TextType.TEXT))
                    
                    # Continue with the rest of the text
                    remaining_text = remaining_text[delimiter_index + len(delimiter):]
                    continue

                # Find the first delimiter
                split_parts = remaining_text.split(delimiter, 1)
                before_delimiter = split_parts[0]
                
                # If there's text before the delimiter, add it
                #if before_delimiter:
                result.append(TextNode(before_delimiter, TextType.TEXT))
                
                # Find the second delimiter
                after_first = split_parts[1]
                
                if after_first == "":  # Nothing after the first delimiter
                    if remaining_text == delimiter:  # Special case: input was exactly the delimiter
                        # Add empty delimited content
                        result.append(TextNode("", text_type))
                        remaining_text = ""
                    else:
                        # Unmatched delimiter
                        raise Exception(f"Invalid markdown: unmatched delimiter '{delimiter}'")
                elif after_first.startswith(delimiter):  # Second delimiter immediately follows
                    # Handle back-to-back delimiters
                    delimited_content = ""
                    result.append(TextNode(delimited_content, text_type))
                    remaining_text = after_first[len(delimiter):]  # Skip past the second delimiter
                else:
                    # Your existing code for finding the second delimiter
                    if delimiter not in after_first:
                        raise Exception(f"Invalid markdown: unmatched delimiter '{delimiter}'")
                    
                    # Split at the second delimiter
                    content_parts = after_first.split(delimiter, 1)
                    delimited_content = content_parts[0]
                    
                    # Add the delimited content with the specified type
                    result.append(TextNode(delimited_content, text_type))
                    
                    # Update remaining text
                    remaining_text = content_parts[1]
            
            # Add any remaining text (even if empty)
            result.append(TextNode(remaining_text, TextType.TEXT))
        
        new_nodes.extend(result)
    
    return new_nodes"""
    """new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Process this text node
        text = old_node.text
        result = []
        i = 0
        #last_end = 0
        start = 0
        in_delimited = False 
        
         # Add initial empty text node if text starts with a delimiter
        if len(text) >= len(delimiter) and text.startswith(delimiter):
            result.append(TextNode("", TextType.TEXT))
             Note: don't update last_end here, it should stay at 0

        if text == "":
            new_nodes.append(old_node)
            continue

        if text == delimiter:
            new_nodes.append(TextNode("", TextType.TEXT))  # Empty text before
            new_nodes.append(TextNode("", text_type))      # Empty bolded text
            new_nodes.append(TextNode("", TextType.TEXT))  # Empty text after
            continue
        
        while i <= len(text) - len(delimiter):
            # Find opening delimiter
            start_index = text.find(delimiter, i)
            # If no more delimiters found, break out of the loop
            if start_index == -1:
                break
                
            # Add the text before the delimiter
            if start_index > last_end:
                result.append(TextNode(text[last_end:start_index], TextType.TEXT))
            elif start_index == last_end and start_index == 0:
                # This handles the case where text starts with delimiter
                result.append(TextNode("", TextType.TEXT))
                
            # Check if this delimiter is escaped
            if start_index > 0 and text[start_index - 1] == '\\':
                # Skip this escaped delimiter and continue searching
                i = start_index + len(delimiter)
                continue

            # Find closing delimiter - we need to find the LAST one
            # Start searching from the position after the opening delimiter
            search_pos = start_index + len(delimiter)
            end_index = -1
            
            while search_pos <= len(text) - len(delimiter):
                next_delimiter = text.find(delimiter, search_pos)
                if next_delimiter == -1:
                    break
                
                # Check if this delimiter is escaped
                if next_delimiter > 0 and text[next_delimiter - 1] == '\\':
                    # Skip this escaped delimiter
                    search_pos = next_delimiter + len(delimiter)
                    continue
                
                # Found a potential closing delimiter
                end_index = next_delimiter
                search_pos = end_index + len(delimiter)
            
            if end_index == -1:
                raise Exception(f"Invalid markdown: unmatched delimiter '{delimiter}'")
                
            # Add text segment before the delimiter
            if start_index >= last_end:
                result.append(TextNode(text[last_end:start_index], TextType.TEXT))
                
            # Add delimited text segment
            delimited_content = text[start_index + len(delimiter):end_index]
            result.append(TextNode(delimited_content, text_type))
            
            # Update positions
            last_end = end_index + len(delimiter)
            i = last_end

            # If this was the last delimiter and it's at the end of the string,
            # add an empty text node
            if last_end == len(text):
                result.append(TextNode("", TextType.TEXT))
        # Add remaining text
        if last_end < len(text):
            result.append(TextNode(text[last_end:], TextType.TEXT))

        # Add the processed nodes
        new_nodes.extend(result)



        
        while i < len(text):
            # Check for escaped delimiter
            if i < len(text) - len(delimiter) + 1 and text[i] == '\\' and text[i+1:i+1+len(delimiter)] == delimiter:
                # Skip the escape character but keep the delimiter
                i += len(delimiter) + 1
            # Check for delimiter
            elif i <= len(text) - len(delimiter) and text[i:i+len(delimiter)] == delimiter:
                # Found a delimiter
                if in_delimited:
                    # End of delimited section
                    result.append(TextNode(text[start:i], text_type))
                    in_delimited = False
                    start = i + len(delimiter)
                    # Add an empty text node if we're at the end
                    if start >= len(text):
                        result.append(TextNode("", TextType.TEXT))
                else:
                    # Start of delimited section
                    result.append(TextNode(text[start:i], TextType.TEXT))
                    in_delimited = True
                i += len(delimiter)
                start = i
            else:
                # Regular character
                i += 1
        
        # Add the remaining text
        if start < len(text):
            if in_delimited:
                # Unclosed delimiter
                raise Exception(f"Invalid markdown: unmatched delimiter '{delimiter}'")
            else:
                result.append(TextNode(text[start:], TextType.TEXT))
        elif in_delimited:
            # Handle case where we ended with an opening delimiter
            raise Exception(f"Invalid markdown: unmatched delimiter '{delimiter}'")
        
        # Add the processed nodes
        new_nodes.extend(result)
    
    return new_nodes"""
    #print(f"Input: {[node.text for node in old_nodes]}")
    """new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        
        for i in range(len(sections)):             

            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))

            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes"""
    """new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        result = []
        current_pos = 0
        
        # If the text starts with a delimiter, add an empty string node first
        if text.startswith(delimiter):
            result.append(TextNode("", TextType.TEXT))
        
        while current_pos < len(text):
            # Find the next opening delimiter
            open_pos = text.find(delimiter, current_pos)
            
            if open_pos == -1:
                # No more delimiters, add remaining text
                result.append(TextNode(text[current_pos:], TextType.TEXT))
                break
            
            # Add text before the delimiter (if we're not at the start of text)
            if open_pos > current_pos:
                result.append(TextNode(text[current_pos:open_pos], TextType.TEXT))
            
            # Find the closing delimiter
            close_pos = text.find(delimiter, open_pos + len(delimiter))
            
            if close_pos == -1:
                # No closing delimiter, this is an error
                raise Exception(f"No closing delimiter '{delimiter}' found")
            
            # Add the content between delimiters
            content = text[open_pos + len(delimiter):close_pos]
            result.append(TextNode(content, text_type))
            
            # Update current position to after the closing delimiter
            current_pos = close_pos + len(delimiter)
        
        new_nodes.extend(result)
    
    return new_nodes"""
    """new_nodes = []

    for old_node in old_nodes:
        print(f"Processing old_node: {old_node.text}")
        if old_node.text_type != TextType.TEXT or old_node.text is None:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        result = []
        current_pos = 0

        # Handle empty text nodes
        if text == "":
            result.append(TextNode("", TextType.TEXT))
        elif text.startswith(delimiter):
            result.append(TextNode("", TextType.TEXT))

        while current_pos < len(text):
            open_pos = text.find(delimiter, current_pos)

            if open_pos == -1:
                result.append(TextNode(text[current_pos:], TextType.TEXT))
                break

            if open_pos > current_pos:
                result.append(TextNode(text[current_pos:open_pos], TextType.TEXT))

            close_pos = text.find(delimiter, open_pos + len(delimiter))

            if close_pos == -1:
                raise Exception(f"No closing delimiter '{delimiter}' found")

            content = text[open_pos + len(delimiter):close_pos]
            result.append(TextNode(content, text_type))

            current_pos = close_pos + len(delimiter)

            if current_pos < len(text) and text[current_pos:current_pos + len(delimiter)] == delimiter:
                result.append(TextNode("", TextType.TEXT))

        if text.endswith(delimiter):
            result.append(TextNode("", TextType.TEXT))

        new_nodes.extend(result)

    print(f"new_nodes: {[node.text for node in new_nodes]}")
    return new_nodes"""
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        
        for i in range(len(sections)):             

            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))

            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes
