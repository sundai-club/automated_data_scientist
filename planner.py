import sys
from pathlib import Path
from autogen import UserProxyAgent, GroupChat, GroupChatManager
from agents.llm_config import llm_config
from agents import all_agents
from tools.rag_engine import rag_query

from dotenv import load_dotenv

_ = load_dotenv(Path(__file__).parent / ".env")


def plan(prompt: str, knowledge_sources_dir: str):

    rag_knowledge = rag_query(prompt, knowledge_sources_dir=knowledge_sources_dir)
    print(f"RAG knowledge: {rag_knowledge}")
    prompt = f"Use the following knowledge sources: {rag_knowledge}\n\n"
    prompt += "Formulate a plan to answer the question.\n\n"

    print(f"Using model: {llm_config['model']}")
    print("Making a plan...")

    groupchat = GroupChat(agents=all_agents, messages=[], max_round=10)
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    user_proxy = UserProxyAgent(
        "user_proxy",
        human_input_mode="NEVER",
        code_execution_config={
            "use_docker": False,
            "enabled": True,
            "last_n_messages": 3,
            "work_dir": "coding",
        },
    )

    user_proxy.initiate_chat(manager, message=prompt)

    print("Plan created!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python plan.py <promptfile> <knowledge_sources_dir>")
        print("Example: python plan.py data/prompt_planner.txt knowledge_sources")
        sys.exit(1)

    promptfile = sys.argv[1]
    knowledge_sources_dir = sys.argv[2]
    prompt = open(promptfile).read()
    plan(prompt, knowledge_sources_dir=knowledge_sources_dir)
