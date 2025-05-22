from langchain.tools import Tool
from mcpadapt.core import MCPAdapt
from utils.crewai_adapter import CrewAIFriendlyAdapter
from mcp import StdioServerParameters
import os

def get_calendar_tools():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_path = os.path.abspath(os.path.join(current_dir, "../mcp/google-calendar-mcp/build/index.js"))

    server = StdioServerParameters(
        command="node",
        args=[mcp_path],
        env=os.environ.copy(),
    )

    with MCPAdapt(server, CrewAIFriendlyAdapter()) as tools:
        return [
            Tool.from_function(
                func=t.func,
                name=t.name,
                description=t.description
            ) for t in tools
        ]