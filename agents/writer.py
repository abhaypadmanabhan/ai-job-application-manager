from crewai import Agent
from tools.cover_letter_tool import cover_letter_tool

def create_writer():
    return Agent(
        role="Cover Letter Writer",
        goal="Write tailored cover letters using the job description and resume.",
        backstory="An expert copywriter specializing in resumes and cover letters.",
        tools=[cover_letter_tool],
        verbose=True
    )