import asyncio
import csv
from typing import List, Dict, Any
import openai
from autogen_agentchat.agents import AssistantAgent
from autogen_core.components.models import OpenAIChatCompletionClient

class ExperimentPlannerAgent:
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(model="gpt-4", api_key=openai.api_key)
        self.planning_assistant = AssistantAgent("planning_assistant", model_client=self.model_client)

    def read_csv_headers(self, file_path: str) -> List[str]:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)
        return headers if headers else []

    async def recommend_analysis(self, headers: List[str]) -> str:
        prompt = f"""Given the following columns in a CSV file:
{', '.join(headers)}

Recommend one simple data analysis task that would be insightful for this dataset. 
The recommendation should be specific and actionable, considering the type of data available.
Provide your recommendation in a single sentence, starting with 'Recommended analysis:'."""

        response = await self.planning_assistant.run(task=prompt)
        return response.strip()

    async def plan_experiment(self, task: str, data_file: str) -> Dict[str, Any]:
        headers = self.read_csv_headers(data_file)
        recommended_analysis = await self.recommend_analysis(headers)

        experiment_plan = {
            "task": task,
            "data_file": data_file,
            "columns": headers,
            "recommended_analysis": recommended_analysis
        }

        return experiment_plan
