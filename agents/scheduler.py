from crewai import Agent
from tools.calendar_mcp_tool import get_calendar_tools

def create_scheduler():
    tools = get_calendar_tools()
    return Agent(
        role="Interview Scheduler",
        goal="Schedule job interview preparation sessions or application reminders.",
        backstory="An assistant that manages Abhay's calendar efficiently.",
        tools=tools,
        verbose=True
    )