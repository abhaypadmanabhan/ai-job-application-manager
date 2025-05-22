from crewai import Agent
from tools.notion_tools import get_notion_tools

def create_logger():
    tools = get_notion_tools()
    return Agent(
        role="Job Tracker",
        goal="Log job application information in Notion for future tracking.",
        backstory="A helpful assistant who never forgets to update the job tracker.",
        tools=tools,
        verbose=True
    )