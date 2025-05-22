# ai-job-application-manager/tools/resume_parser_tool.py
import os
from smolagents import tool
from dotenv import load_dotenv # For testing this file directly

@tool
def load_resume_text(file_path: str = "data/abhay_padmanabhan.txt") -> str:
    """
    Loads the text content from a specified resume file.
    Defaults to "data/abhay_padmanabhan.txt" if no path is provided.

    Args:
        file_path: The relative or absolute path to the resume text file.

    Returns:
        The text content of the resume file as a string, or an error message string if not found/readable.
    """
    # Ensure the path is constructed correctly, assuming the agent might provide
    # a path relative to the project root or an absolute path.
    # For simplicity, we'll assume file_path is relative to the project root if not absolute.
    
    # Construct path relative to project root if file_path is not absolute
    # This assumes tools are run from the project root context (e.g., via `python -m workflows.apply_and_log`)
    if not os.path.isabs(file_path):
        # This gets the current working directory, which should be the project root
        # when `python -m workflows.apply_and_log` is used.
        project_root = os.getcwd() 
        actual_path = os.path.join(project_root, file_path)
    else:
        actual_path = file_path

    print(f"[load_resume_text tool] Attempting to load resume from: {actual_path}")
    if not os.path.exists(actual_path):
        error_msg = f"Error: Resume file not found at {actual_path}. Please ensure the file exists or the path is correct relative to the project root."
        print(f"[load_resume_text tool] {error_msg}")
        return error_msg
    
    try:
        with open(actual_path, 'r', encoding='utf-8') as f:
            resume_content = f.read()
        print(f"[load_resume_text tool] Successfully loaded resume. Length: {len(resume_content)} characters.")
        return resume_content
    except Exception as e:
        error_msg = f"Error reading resume file at {actual_path}: {str(e)}"
        print(f"[load_resume_text tool] {error_msg}")
        return error_msg

if __name__ == '__main__':
    load_dotenv() # Not strictly needed for this tool unless it uses env vars, but good practice

    print("--- Testing load_resume_text tool ---")
    
    # Test with default path (ensure data/abhay_padmanabhan.txt exists relative to project root)
    print("\nTest 1: Loading with default file path...")
    # To run this test directly, cd to the project root first, then run python tools/resume_parser_tool.py
    # OR adjust the default path temporarily for direct testing if needed
    # For this test script, let's assume it's run from project root or paths are adjusted.
    # If your data folder is `ai-job-application-manager/data/abhay_padmanabhan.txt`
    # and you run `python tools/resume_parser_tool.py` from `ai-job-application-manager`
    # the default path "data/abhay_padmanabhan.txt" should work.

    # To make the direct test more robust if run from tools/ directory:
    default_resume_path_for_test = "../data/abhay_padmanabhan.txt" # Relative to tools/ directory
    # Check if the file exists using this relative path for the test
    if not os.path.exists(default_resume_path_for_test):
        print(f"Test Warning: {default_resume_path_for_test} not found. Default path might be incorrect for direct script run from tools/ folder.")
        print("Attempting with assumed project root default data/abhay_padmanabhan.txt")
        # Try the path as if 'tools' is a subdir of where 'data' is
        project_data_path = os.path.join(os.path.dirname(os.getcwd()), "data", "abhay_padmanabhan.txt")
        if os.path.exists(project_data_path):
            print(f"Found at {project_data_path}")
            resume1 = load_resume_text(project_data_path)
        else: # Fallback to the default for when run with `python -m`
             resume1 = load_resume_text() # Uses default "data/abhay_padmanabhan.txt"
    else:
        resume1 = load_resume_text(default_resume_path_for_test)


    if "Error:" not in resume1:
        print(f"Resume 1 (first 100 chars): {resume1[:100]}...")
    else:
        print(resume1)

    # Test with a non-existent file
    print("\nTest 2: Loading with a non-existent file path...")
    resume2 = load_resume_text("data/non_existent_resume.txt")
    print(resume2)

    # Test with an absolute path (you'll need to create this file or change path for your system)
    # For example, create /tmp/my_test_resume.txt with some content
    # test_absolute_path = "/tmp/my_test_resume.txt" 
    # with open(test_absolute_path, "w") as f_tmp:
    # f_tmp.write("This is a test resume from an absolute path.")
    # print("\nTest 3: Loading with an absolute file path (requires /tmp/my_test_resume.txt)...")
    # resume3 = load_resume_text(test_absolute_path)
    # if "Error:" not in resume3:
    # print(f"Resume 3: {resume3}")
    # else:
    # print(resume3)
    # if os.path.exists(test_absolute_path):
    # os.remove(test_absolute_path)