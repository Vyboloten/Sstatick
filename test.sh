#python3 -m unittest discover -s src
#python3 -m unittest discover src -v
#python3 -m unittest src.test_htmlnode -v
#python3 -m test_textnode.Test_text_node_to_html_node
#python3 -m unittest src.test_textnode.Test_text_node_to_html_node -v

export PYTHONPATH=.

# Run the tests
#python3 -m unittest src.test_textnode.Test_text_node_to_html_node -v
#python3 -m unittest src.test_text_splitter.TestSplitNodesDelimiter -v
#python3 -m unittest src.test_markdown_extractor.TestBlockSplitter -v
#python3 -m unittest src.test_blocktype.TestBlockToBlockType -v
python3 -m unittest src.new_test -v
#python3 -m unittest src.test_blocktype.TestMarkdownToHtmlNode -v


#python3 -m unittest src.test_textnode.Test_text_node_to_html_node src.test_htmlnode.TestHTMLNode
# Check if tests succeeded
if [ $? -eq 0 ]; then
    echo "Tests passed successfully!"
    exit 0
else
    echo "Tests failed!"
    exit 1
fi