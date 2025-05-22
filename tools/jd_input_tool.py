# ai-job-application-manager/tools/jd_input_tool.py
import os
from smolagents import tool
from dotenv import load_dotenv

@tool
def load_text_from_file(file_path: str) -> str:
    """
    Loads the text content from a specified file.
    Use this to load job descriptions or other text inputs saved in files.

    Args:
        file_path: The relative (to project root) or absolute path to the text file.

    Returns:
        The text content of the file as a string, or an error message string if not found/readable.
    """
    if not os.path.isabs(file_path):
        project_root = os.getcwd() 
        actual_path = os.path.join(project_root, file_path)
    else:
        actual_path = file_path

    print(f"[load_text_from_file tool] Attempting to load text from: {actual_path}")
    if not os.path.exists(actual_path):
        error_msg = f"Error: File not found at {actual_path}."
        print(f"[load_text_from_file tool] {error_msg}")
        return error_msg
    
    try:
        with open(actual_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"[load_text_from_file tool] Successfully loaded text. Length: {len(content)} characters.")
        return content
    except Exception as e:
        error_msg = f"Error reading file at {actual_path}: {str(e)}"
        print(f"[load_text_from_file tool] {error_msg}")
        return error_msg

if __name__ == '__main__':
    load_dotenv()
    print("--- Testing load_text_from_file tool ---")

    # Create a dummy JD file for testing in data/
    test_jd_content = "Seeking a Senior Python Developer with 5+ years of experience in web frameworks (Django/Flask), API design, and cloud platforms (AWS/Azure). Strong problem-solving skills and experience with Agile methodologies required. Familiarity with Docker and Kubernetes is a plus."
    jd_file_path_relative = "data/sample_jd.txt"
    
    # Construct path assuming this test is run from project root
    project_root_dir = os.getcwd() # Or os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if always running from tools
    if "tools" in project_root_dir: # If CWD is tools/
        project_root_dir = os.path.dirname(project_root_dir)

    full_jd_file_path = os.path.join(project_root_dir, jd_file_path_relative)
    
    data_dir = os.path.join(project_root_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created directory: {data_dir}")

    try:
        with open(full_jd_file_path, "w", encoding="utf-8") as f:
            f.write(test_jd_content)
        print(f"Created/Updated test JD file at: {full_jd_file_path}")
    except Exception as e:
        print(f"Error creating test JD file: {e}")


    print(f"\nTest 1: Loading JD from '{jd_file_path_relative}'...")
    # When running from project root, 'data/sample_jd.txt' should be passed
    jd_text = load_text_from_file(jd_file_path_relative) 
    if "Error:" not in jd_text:
        print(f"JD Text (first 100 chars): {jd_text[:100]}...")
    else:
        print(jd_text)