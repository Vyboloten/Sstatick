#print("hello world")
#from src.htmlnode import HTMLNode, LeafNode, ParentNode
#from src.textnode import TextNode, TextType
import os, shutil, sys
#print("Current working directory:", os.getcwd())
#print(os.path.exists("/root/workspace/github.com/Vyboloten/Sstatick/src/utils.py"))
from src.utils import copy_files_recursive, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"
dir_path_docs = "./docs"

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

def main():
    # First delete public if it exists
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)
        print("Deleted existing docs directory.")
    # Then call your function with static as source and public as destination
    #copy_static('static', 'public')
     # Create markdown files
    #create_index_md()
    #create_markdown_files()
    #copy_images ()
    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)
    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)
    # Generate HTML pages for all markdown files
    """for root, dirs, files in os.walk("content"):
        for file in files:
            if file.endswith(".md"):
                markdown_path = os.path.join(root, file)
                # Determine the output path
                rel_path = os.path.relpath(markdown_path, "content")
                output_path = os.path.join("public", os.path.splitext(rel_path)[0] + ".html")
                
                # Create the directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Generate the HTML page
                generate_page(markdown_path, "template.html", output_path)
                print(f"Generated HTML page at {output_path}")"
                """
    

        



# Call the main function
if __name__ == "__main__":
    main()