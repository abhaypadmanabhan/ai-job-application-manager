# ai-job-application-manager/workflows/apply_and_log.py
import os
from dotenv import load_dotenv

from smolagents import LiteLLMModel
from agents.manager_agent import ManagerAgent

# Import tool functions from their respective files
from tools.file_tools import create_file
from tools.web_scraping_tools import scrape_job_board
from tools.notion_tools import append_text_to_notion_page
from tools.resume_parser_tool import load_resume_text
from tools.jd_input_tool import load_text_from_file
from tools.compatibility_analyzer_tool import analyze_resume_jd_match
from tools.cover_letter_tool import draft_cover_letter
from tools.resume_tuner_tool import suggest_resume_improvements

def main():
    load_dotenv() 

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    notion_api_key = os.getenv("NOTION_API_KEY") 
    notion_page_id_for_logging = os.getenv("NOTION_PAGE_ID_FOR_LOGGING")

    if not gemini_api_key: print("Warning: GEMINI_API_KEY not found in .env.")
    if not notion_api_key: print("Warning: NOTION_API_KEY not found in .env. Needed for notion_tools.py.")
    if not notion_page_id_for_logging: print("Warning: NOTION_PAGE_ID_FOR_LOGGING not found in .env. Agent will need this ID to log to the page.")

    llm_model = LiteLLMModel(
        model_id="gemini/gemini-1.5-flash-latest"
    )

    available_tools = [
        create_file,
        scrape_job_board,
        append_text_to_notion_page,
        load_resume_text,
        load_text_from_file,
        analyze_resume_jd_match,
        draft_cover_letter,
        suggest_resume_improvements, # <<< --- ADD THE NEW TOOL HERE
    ]

    manager = ManagerAgent(
        model=llm_model,
        tools=available_tools,
    )

    print("-" * 50)
    print("AI Job Application Manager Workflow Started (Appending to Notion Page).")
    print(f"Using LLM: {llm_model.model_id}")
    print(f"Notion Page ID for logging (from .env): {notion_page_id_for_logging if notion_page_id_for_logging else 'NOT SET - Agent will need this ID!'}")
    print(f"Total tools loaded: {len(available_tools)}") # Should now show 4
    print("Type 'exit' or 'quit' to end.")
    print("Example task: Load my resume and tell me the first 50 characters.")
    # Update example task if needed
    print("-" * 50)

    while True:
        user_task = input("\nEnter your task: ")
        if user_task.lower() in ['exit', 'quit']:
            print("Exiting Job Application Manager.")
            break

        manager.run_task(user_task)

if __name__ == "__main__":
    main()