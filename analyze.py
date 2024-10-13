import os
import sys
from pathlib import Path
from autogen import (
    UserProxyAgent,
    GroupChat,
    GroupChatManager,
    AssistantAgent,
    ConversableAgent,
)
from autogen.coding.jupyter import JupyterCodeExecutor, LocalJupyterServer
from agents.llm_config import llm_config
from agents import all_agents
from typing_extensions import Annotated
from ipynb import append_code_to_ipynb

from dotenv import load_dotenv

_ = load_dotenv(Path(__file__).parent / ".env")


def analyze(prompt: str, datafile: str):

    prompt += f"\n\nUse data from '{datafile}'."
    prompt += "\n\nSave the analysis as a ipynb file."

    print(f"Using model: {llm_config['model']}")
    print("Analyzing data...")

    simple_agent = AssistantAgent(name="Assistant", llm_config=llm_config)

    # The code writer agent's system message is to instruct the LLM on how to
    # use the Jupyter code executor with IPython kernel.
    code_writer_system_message = """
You have been given coding capability to solve tasks using Python code in a stateful IPython kernel.
You are responsible for writing the code, and the user is responsible for executing the code.

When you write Python code, put the code in a markdown code block with the language set to Python.
For example:
```python
x = 3
```
You can use the variable `x` in subsequent code blocks.
```python
print(x)
```

Write code incrementally and leverage the statefulness of the kernel to avoid repeating code.
Import libraries in a separate code block.
Define a function or a class in a separate code block.
Run code that produces output in a separate code block.
Run code that involves expensive operations like download, upload, and call external APIs in a separate code block.

When your code produces an output, the output will be returned to you.
Because you have limited conversation memory, if your code creates an image,
the output will be a path to the image instead of the image itself."""

    server = LocalJupyterServer()

    os.makedirs("output", exist_ok=True)

    code_executor_agent = ConversableAgent(
        name="code_executor_agent",
        llm_config=False,
        code_execution_config={
            "executor": JupyterCodeExecutor(server, output_dir="output"),
        },
        human_input_mode="NEVER",
    )

    code_writer_agent = ConversableAgent(
        name="code_writer",
        system_message=code_writer_system_message,
        llm_config=llm_config,
        code_execution_config=False,  # Turn off code execution for this agent.
        max_consecutive_auto_reply=2,
        human_input_mode="NEVER",
    )

    functions = [
        {
            "name": "save_as_jupyther",
            "description": "Appends Python code to an existing .ipynb Jupyter Notebook file, or creates a new one if it doesn't exist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code_str": {
                        "type": "string",
                        "description": "A string containing Python code.",
                    }
                },
                "required": ["code_str"],
            },
        }
    ]

    save_as_jupyther = ConversableAgent(
        name="save_as_jupyther",
        system_message="I'm SaveAsJupyter. I will save the analysis as a Jupyter notebook.",
        llm_config=llm_config | {"functions": functions},
    )

    save_as_jupyther.register_function(
        function_map={
            "save_as_jupyther": append_code_to_ipynb,
        },
    )

    # engineer = AssistantAgent(
    #     name="Engineer",
    #     llm_config=llm_config,
    #     system_message="I'm Engineer. I'm expert in python programming. I'm executing code tasks required by others.",
    # )

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

    # @engineer.register_for_llm(description="Check the contents of a chosen file.")
    # def see_file(filename: Annotated[str, "Name and path of file to check."]):
    #     with open(Path(__file__).parent + filename, "r") as file:
    #         lines = file.readlines()
    #     formatted_lines = [f"{i+1}:{line}" for i, line in enumerate(lines)]
    #     file_contents = "".join(formatted_lines)

    #     return 0, file_contents

    # user_proxy.register_for_execution(see_file)

    agents = [code_writer_agent, code_executor_agent, save_as_jupyther]
    groupchat = GroupChat(agents=agents, messages=[], allow_repeat_speaker=False)

    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    user_proxy.initiate_chat(manager, message=prompt)

    server.stop()

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
