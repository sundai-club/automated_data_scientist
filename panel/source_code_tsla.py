import panel as pn
import autogen
import os
import io
import uuid
import re
import traceback
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

pn.extension(design="material")

# Define configurations for AutoGen
config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4"],
    },
)

llm_config = {"config_list": config_list_gpt4, "seed": 42, "api_type": "openai"}

code_execution_config = {
    "use_docker": False
}

# Adjusted agent settings to be more concise and target-driven
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 3, "work_dir": "groupchat", "use_docker": False},
    human_input_mode="NEVER",
)

coder = autogen.AssistantAgent(
    name="Coder",
    system_message=(
        "You are a helpful assistant. Provide clear and concise answers to the user's questions. "
        "When providing code, ensure it is executable in the local environment and that any plots "
        "are saved to files and displayed in the UI. Avoid unnecessary conversation."
    ),
    llm_config=llm_config,
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message=(
        "As a Critic, evaluate the quality of the provided financial visualization code on a scale "
        "from 1 (bad) to 10 (good), and provide clear rationale. Once you are satisfied with the "
        "code, confirm your approval."
    ),
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=5)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

def execute_code(code: str, plot_path: str):
    """Executes the given code and captures any plots generated."""
    local_vars = {}
    try:
        # Ensure plot_path uses forward slashes to avoid escape issues
        plot_path = plot_path.replace('\\', '/')

        # Replace plt.show() with plt.savefig()
        code = re.sub(r'plt\.show\s*\(\s*\)', f'plt.savefig(r"{plot_path}")\nplt.close()', code)

        # If plt.savefig is not in the code, append it
        if 'plt.savefig' not in code:
            code += f'\nplt.savefig(r"{plot_path}")\nplt.close()'

        # Execute the code
        exec(code, {"pd": pd, "plt": plt, "np": np, "sns": sns, "__name__": "__main__"}, local_vars)
        return "Code executed successfully."
    except Exception as e:
        return f"Code execution failed:\n{traceback.format_exc()}"

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    # Use AutoGen to process the message
    user_proxy.initiate_chat(
        manager,
        message=f"Download data from C:/Users/lenovo/Desktop/hackathon/automated_data_scientist/panel/TSLA.csv and {contents}"
    )

    # Get the assistant's final answer
    assistant_response = ""
    for message in reversed(groupchat.messages):
        if isinstance(message, tuple):
            agent, content = message
            if agent.name == 'Coder':
                assistant_response = content
                break
        elif isinstance(message, dict):
            if message.get('name') == 'Coder':
                assistant_response = message['content']
                break

    # Extract code blocks from the assistant's message
    code_blocks = re.findall(r'```python(.*?)```', assistant_response, re.DOTALL)

    # Execute the code blocks and capture plots
    for code in code_blocks:
        # Generate a unique filename for the plot
        plot_filename = f"plot_{uuid.uuid4().hex}.png"
        plot_path = os.path.join("groupchat", plot_filename)

        # Ensure the groupchat directory exists
        os.makedirs("groupchat", exist_ok=True)

        # Replace file paths in the code with your local CSV path
        code = re.sub(
            r'pd\.read_csv\([\'\"].*?[\'\"]\)',
            'pd.read_csv(r"C:/Users/lenovo/Desktop/hackathon/automated_data_scientist/panel/TSLA.csv")',
            code
        )

        # Execute the code
        execution_result = execute_code(code.strip(), plot_path)

        # If the plot was generated, display it
        if os.path.exists(plot_path):
            panel_img = pn.pane.Image(plot_path, width=600)
            instance.stream(panel_img, user="System")

    # Remove code blocks and technical details from the assistant's message
    assistant_response_clean = re.sub(r'```python.*?```', '', assistant_response, flags=re.DOTALL).strip()

    # Display only the assistant's final answer
    return assistant_response_clean

chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send(
    "What would you like to do?",
    user="System",
    respond=False,
)
chat_interface.servable()
