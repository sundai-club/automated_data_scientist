# agents/coding_agent.py

import asyncio
import json
from typing import Dict, Any
import openai
from autogen_agentchat.agents import CodingAssistantAgent
from autogen_core.components.models import OpenAIChatCompletionClient

class CodingAgent:
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(model="gpt-4", api_key=openai.api_key)
        self.coding_assistant = CodingAssistantAgent("coding_assistant", model_client=self.model_client)

    async def generate_code(self, experiment_plan: Dict[str, Any]) -> str:
        prompt = f"Generate Python code for the following experiment plan:\n{json.dumps(experiment_plan, indent=2)}\n\nInclude necessary imports and ensure the code is ready to run."
        
        response = await self.coding_assistant.run(task=prompt)
        
        # Extract the code from the response
        code = self._extract_code_from_response(response)
        
        return code

    def _extract_code_from_response(self, response: str) -> str:
        # Simple extraction: assume the code is between triple backticks
        code_blocks = response.split("```")
        if len(code_blocks) >= 3:
            return code_blocks[1].strip()
        return response  # Return full response if no code block is found

    async def save_code_to_file(self, code: str, filename: str = "generated_code.py"):
        with open(filename, "w") as file:
            file.write(code)
        print(f"Code saved to {filename}")

    async def process_experiment(self, experiment_plan: Dict[str, Any]) -> Dict[str, str]:
        generated_code = await self.generate_code(experiment_plan)
        await self.save_code_to_file(generated_code)
        return {
            "generated_code": generated_code,
            "code_file": "generated_code.py"
        }