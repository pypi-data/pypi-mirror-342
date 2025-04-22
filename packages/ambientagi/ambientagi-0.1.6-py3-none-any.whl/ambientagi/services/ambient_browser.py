# flake8: noqa: E402
import os

os.environ["BROWSER_USE_LOGGING_LEVEL"] = "result"  # noqa: E402

from typing import Optional

from browser_use import Agent  # type: ignore
from langchain_openai import ChatOpenAI  # type: ignore

from ambientagi.config.settings import settings


class BrowserAgent:
    def __init__(self, agent: dict):
        """
        Initialize the BrowserAgent
        """
        self.name = agent["agent_name"]
        self.wallet_address = agent["wallet_address"]
        self.task = agent["description"]

        print("Initialized BrowserAgent for ", self.name)

    async def run_task(self, task: Optional[str] = None, model: str = "gpt-4o"):
        """
        Run the agent's task after ensuring the user is registered.

        :param task: The task to perform. If not provided, use the default task.
        :param model: The LLM model to use (default is 'gpt-4o').
        :return: Result of the task execution.
        """

        # Use the default task if none is provided
        task = task or self.task

        # Initialize the agent and run the task
        agent = Agent(
            task=task, llm=ChatOpenAI(model=model, api_key=settings.OPENAI_KEY)
        )
        result = await agent.run()
        return result
