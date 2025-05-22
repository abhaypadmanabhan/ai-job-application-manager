from langchain.tools import Tool

# Use Tool from LangChain as-is; no need to redefine it
# So you can delete your current custom Tool class
class Tool:
    def __init__(self, name: str, description: str, func: callable):
        self.name = name
        self.description = description
        self.func = func

    def run(self, input: dict) -> str:
        return self.func(input)