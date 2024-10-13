import sys
from pathlib import Path
from autogen import UserProxyAgent, GroupChat, GroupChatManager
from agents.llm_config import llm_config
from agents import all_agents

from dotenv import load_dotenv

_ = load_dotenv(Path(__file__).parent / ".env")


def analyze(prompt: str, datafile: str):

    prompt += f"Use data from '{datafile}'.\n\n"
    prompt += "Output the analysis in a ipynb file.\n\n"

    print(f"Using model: {llm_config['model']}")
    print("Analyzing data...")

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

    print("Data analyzed!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analyze.py <promptfile> <datafile>")
        print("Example: python analyze.py data/prompt.txt data/data.vcf")
        sys.exit(1)

    promptfile = sys.argv[1]
    datafile = sys.argv[2]
    prompt = open(promptfile).read()
    analyze(prompt, datafile)
