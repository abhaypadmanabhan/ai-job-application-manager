# ai-job-application-manager/agents/manager_agent.py

from smolagents import CodeAgent, LiteLLMModel

class ManagerAgent(CodeAgent):
    def __init__(self, model: LiteLLMModel, tools: list,
                 additional_authorized_imports: list = None,
                 **other_code_agent_kwargs):

        # This is a guiding prompt for us or for prepending to tasks if needed.
        # CodeAgent will use its own internal prompting mechanisms primarily.
        self.custom_guidance_prompt = """
You are an expert Job Application Assistant. Your primary goal is to help the user manage their job application process.
You have access to a variety of tools to find job openings, interact with Notion, create files, and eventually draft documents.
Plan your steps carefully and use the provided tools to achieve the user's tasks.
When using tools, ensure you provide all required arguments correctly based on their descriptions.
After performing actions, provide a clear summary of what you did and the outcome.
If you encounter an error with a tool, report the error clearly.
"""
        effective_additional_imports = additional_authorized_imports
        if effective_additional_imports is None:
            effective_additional_imports = ["os", "json", "requests", "bs4", "urllib.parse", "datetime", "time"]

        # Ensure 'system_prompt' is not in other_code_agent_kwargs if it was accidentally passed
        if 'system_prompt' in other_code_agent_kwargs:
            del other_code_agent_kwargs['system_prompt']
        if 'system_prompt_text' in other_code_agent_kwargs:
            del other_code_agent_kwargs['system_prompt_text']

        super().__init__(
            tools=tools,
            model=model,
            additional_authorized_imports=effective_additional_imports,
            **other_code_agent_kwargs # Pass only known, valid kwargs for CodeAgent here
        )
        print(f"[ManagerAgent] Initialized. Custom guidance prompt (for reference): \"{self.custom_guidance_prompt[:70].strip()}...\"")


    def run_task(self, task: str):
        print(f"\n[ManagerAgent] Received task: {task}")
        print("[ManagerAgent] Thinking...")
        
        # For now, we pass the task directly. CodeAgent's internal prompt will guide it.
        # If needed, we could prepend self.custom_guidance_prompt here.
        effective_task = task

        try:
            result = self.run(effective_task) # self.run() is from the parent CodeAgent
            print("\n[ManagerAgent] Task Result:")
            print(result)
            return result
        except Exception as e:
            print(f"[ManagerAgent] Error during task execution: {e}")
            import traceback
            traceback.print_exc()
            return f"Error: {e}"

if __name__ == '__main__':
    # This block is for quick, isolated testing of ManagerAgent if needed.
    # The main workflow is in workflows/apply_and_log.py
    from dotenv import load_dotenv
    import os

    print("Running ManagerAgent direct test...")
    load_dotenv() 

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file for direct test.")

    llm_model = LiteLLMModel(
        model_id="gemini/gemini-1.5-flash-latest"
    )

    # For direct testing, you'd need to import and decorate dummy tools here or actual tools
    from smolagents import tool
    @tool
    def dummy_scrape(url: str) -> str:
        """Scrapes a URL (dummy)."""
        return f"Scraped {url}, found dummy data."

    test_manager = ManagerAgent(model=llm_model, tools=[dummy_scrape])

    print("ManagerAgent initialized for direct testing.")
    while True:
        user_task = input("\nEnter task for ManagerAgent (direct test - or 'exit' to quit): ")
        if user_task.lower() == 'exit':
            break
        test_manager.run_task(user_task)