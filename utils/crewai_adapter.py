import re
from mcpadapt.core import ToolAdapter

class CrewAIFriendlyAdapter(ToolAdapter):
    def adapt(self, func, tool):
        tool.name = re.sub(r'\W|^(?=\d)', '_', tool.name)
        return super().adapt(func, tool)