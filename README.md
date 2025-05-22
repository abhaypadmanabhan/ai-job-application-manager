# AI-Powered Job Application Manager

## Overview

This project is an AI-driven Job Application Manager designed to streamline and automate various aspects of the job application process. It leverages Python, the `smol-agents` framework, and Google's Gemini LLM to provide intelligent assistance. Key functionalities include analyzing resume-to-job-description compatibility, drafting tailored cover letters, offering resume enhancement suggestions, and logging all activities to a designated Notion page.

The system operates through a `ManagerAgent` that orchestrates various custom-built Python tools. These tools handle tasks such as document parsing (resumes, job descriptions), making LLM calls for analysis and content generation, interacting with the local file system for saving documents, and integrating with the Notion API for logging.

## Features

* **Resume Loading:** Loads candidate's resume from a local text file.
* **Job Description Loading:** Loads job descriptions from local text files (current) or via web scraping (local HTML files).
* **Resume-JD Compatibility Analysis:** Utilizes an LLM (Gemini) to:
    * Calculate a compatibility score.
    * Identify strengths and weaknesses of the resume against the JD.
    * Perform keyword matching.
    * Provide an overall summary of the candidate's fit.
* **Cover Letter Drafting:** Generates a tailored cover letter using the resume, JD, and compatibility analysis insights.
* **Resume Improvement Suggestions:** Provides actionable suggestions to enhance the resume for a specific job, based on the compatibility analysis.
* **Document Saving:** Saves generated cover letters and resume suggestions to the local file system.
* **Notion Logging:** Appends a summary of all processed actions (job details, analysis score, paths to saved documents) to a specified Notion page for tracking.
* **Agentic Workflow:** Uses a `ManagerAgent` to interpret natural language commands and orchestrate the sequence of tool usage.

## Technologies Used

* **Programming Language:** Python 3.10+
* **AI Agent Framework:** `smol-agents`
* **Large Language Model (LLM):** Google Gemini (specifically `gemini-1.5-flash-latest` via `litellm`)
* **Core Libraries:**
    * `python-dotenv`: For managing environment variables.
    * `requests`: For HTTP requests (used in web scraping tool).
    * `beautifulsoup4`: For HTML parsing (used in web scraping tool).
    * `notion-client`: For direct interaction with the Notion API.
    * `litellm`: For standardized interaction with LLMs.
* **Development Environment:** Managed with a Python virtual environment (`venv`).

## Project Structure
ai-job-application-manager/
├── .env                  # For API keys and configuration (create this)
├── agents/               # Contains agent definitions (e.g., ManagerAgent)
│   ├── init.py
│   └── manager_agent.py
├── data/                 # For storing resume, sample JDs, etc.
│   └── abhay_padmanabhan.txt
│   └── sample_jd.txt
├── output_documents/     # For saving generated cover letters, suggestions (created by agent)
├── tools/                # Contains individual tool scripts
│   ├── init.py
│   ├── file_tools.py
│   ├── jd_input_tool.py
│   ├── notion_tools.py
│   ├── resume_parser_tool.py
│   ├── compatibility_analyzer_tool.py
│   ├── cover_letter_tool.py
│   └── web_scraping_tools.py
│   └── resume_tuner_tool.py
├── workflows/            # Contains main workflow orchestration scripts
│   ├── init.py
│   └── apply_and_log.py
├── test_jobs.html        # Sample HTML for testing web scraper (created by web_scraping_tools.py)
└── requirements.txt      # Python dependencies

## Setup Instructions

1.  **Prerequisites:**
    * Python 3.10 or higher.
    * `pip` (Python package installer).

2.  **Clone the Repository (Example):**
    ```bash
    git clone <your-repository-url>
    cd ai-job-application-manager
    ```

3.  **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up Environment Variables:**
    Create a `.env` file in the project root directory (`ai-job-application-manager/.env`) and add the following, replacing placeholders with your actual values:
    ```env
    GEMINI_API_KEY=your_google_gemini_api_key
    NOTION_API_KEY=your_notion_integration_token
    NOTION_PAGE_ID_FOR_LOGGING=your_notion_page_id_for_appending_logs
    ```
    * `GEMINI_API_KEY`: Your API key for Google Gemini.
    * `NOTION_API_KEY`: Your Notion integration token (secret).
    * `NOTION_PAGE_ID_FOR_LOGGING`: The ID of the Notion page where the agent will append its logs.

6.  **Notion Setup:**
    * Ensure the Notion page specified by `NOTION_PAGE_ID_FOR_LOGGING` exists.
    * Share this Notion page with your integration (the one associated with your `NOTION_API_KEY`). Grant it "Can edit" or "Can edit content" permissions.

7.  **Prepare Your Resume:**
    * Place your resume text in `data/abhay_padmanabhan.txt` (or update the default path in `tools/resume_parser_tool.py` and agent prompts).

## How to Run

1.  **Activate Virtual Environment:**
    ```bash
    source venv/bin/activate # Or venv\Scripts\activate
    ```

2.  **Test Individual Tools (Recommended):**
    You can test each tool directly from the project root to ensure they are functioning correctly before running the full workflow:
    ```bash
    python tools/file_tools.py
    python tools/resume_parser_tool.py
    python tools/jd_input_tool.py  # This will create data/sample_jd.txt if not present
    python tools/web_scraping_tools.py # This will create test_jobs.html if not present
    python tools/compatibility_analyzer_tool.py # Needs GEMINI_API_KEY
    python tools/cover_letter_tool.py # Needs GEMINI_API_KEY
    python tools/resume_tuner_tool.py # Needs GEMINI_API_KEY
    python tools/notion_tools.py # Needs NOTION_API_KEY and NOTION_PAGE_ID_FOR_LOGGING
    ```

3.  **Run the Main Workflow:**
    Execute the main application script from the project root directory:
    ```bash
    python -m workflows.apply_and_log
    ```

4.  **Interact with the Agent:**
    The script will start, and you'll be prompted to `Enter your task:`.
    Provide detailed, multi-step instructions. For example:

    ```
    Load my resume.
    Load the job description from 'data/sample_jd.txt'.
    Analyze the resume against the JD.
    Draft a cover letter for the 'Junior Data Scientist - AI Team' position at 'Innovatech Solutions Inc.' using my resume, the loaded JD, and the compatibility analysis. Save the drafted cover letter to a file named 'cover_letter_innovatech.txt' inside a folder named 'output_documents'.
    Then, using the analysis, suggest improvements for my resume to better fit this job. Save these suggestions to a file named 'resume_suggestions_innovatech.txt' inside the 'output_documents' folder.
    Finally, append a log entry to Notion page 'YOUR_NOTION_PAGE_ID' summarizing these actions, including the compatibility score, and mentioning the filenames of the saved documents.
    ```
    (Remember to replace `YOUR_NOTION_PAGE_ID` with your actual Notion Page ID if it's different from what's in `.env` or if you want to override it in the prompt).

## Current Status

* Core functionalities for resume/JD loading, compatibility analysis, cover letter drafting, resume suggestions, file saving, and Notion logging are implemented and working.
* Job scraping is currently limited to local HTML files; robust scraping of live job boards is a future enhancement.
* The agent successfully orchestrates multiple tools based on natural language commands.

## Future Work (Potential Enhancements)

* **Advanced Web Scraping:** Integrate Selenium/Playwright for scraping dynamic job sites (e.g., LinkedIn, Indeed) or use official job board APIs if available.
* **Interactive UI:** Develop a web interface (e.g., using Streamlit or Flask) for easier interaction.
* **Direct Application (Highly Complex):** Explore possibilities for assisting with filling out online application forms (would be site-specific and challenging).
* **Interview Preparation Module:** Add tools to generate potential interview questions and help structure answers.
* **More Sophisticated Notion Integration:** Use Notion databases for structured tracking instead of appending to a single page, allowing for better filtering and status management.
* **Resume Parsing from PDF/DOCX:** Add tools to directly parse resume content from common file formats beyond plain text.
