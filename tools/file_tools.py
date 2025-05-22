# ai-job-application-manager/tools/file_tools.py
import os
from smolagents import tool

@tool
def create_file(path: str, content: str) -> str:
    """
    Creates a file at the specified path with the given content.
    If directories in the path do not exist, they will be created.

    Args:
        path: The filesystem path (including filename) where the file will be created.
        content: The text content to write into the file.
    
    Returns:
        A string indicating success or failure.
    """
    try:
        dir_name = os.path.dirname(path)
        if dir_name: # Only create directories if a path component exists
            os.makedirs(dir_name, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File created successfully at {path}"
    except Exception as e:
        return f"Error creating file at {path}: {e}"

if __name__ == '__main__':
    # Test the tool
    # Create a test_output directory if it doesn't exist for the output
    if not os.path.exists("test_output"):
        os.makedirs("test_output")
    print(create_file("test_output/sample_from_file_tools.txt", "Hello from file_tools.py direct test!"))
    print(create_file("another_sample.txt", "Hello, world! This file is in the root if run from root."))