from agents.llm_config import llm_config
from autogen import AssistantAgent

# please define agent in your script, it will be used in analyze.py
simple_agent = AssistantAgent("assistant", llm_config=llm_config)
