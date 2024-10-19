from agents.llm_config import llm_config
from autogen import AssistantAgent
from agents.custom_personas import PlanningAgent, CodingAgent, StatisticsAgent

# please define agent in your script, it will be used in analyze.py
simple_agent = AssistantAgent("assistant", llm_config=llm_config)
planning_agent = PlanningAgent("planning_agent", llm_config=llm_config)
coding_agent = CodingAgent("coding_agent", llm_config=llm_config)
statistics_agent = StatisticsAgent("statistics_agent", llm_config=llm_config)
