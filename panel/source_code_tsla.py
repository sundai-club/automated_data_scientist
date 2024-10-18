import panel as pn
import autogen
import os
import io
from PIL import Image

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

user_proxy = autogen.UserProxyAgent(
   name="User_proxy",
   system_message="A human admin.",
   code_execution_config={"last_n_messages": 3, "work_dir": "groupchat", "use_docker": False},
   human_input_mode="NEVER",
)
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
)
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="""Critic. You are a helpful assistant highly skilled in evaluating the quality of a given financial visualization code by providing a score from 1 (bad) - 10 (good) while providing clear rationale...""",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    # Use AutoGen to process the message
    user_proxy.initiate_chat(
        manager,
        message=f"Download data from /Users/ai/Documents/sundai/automated-data-scientist/panel/TSLA.csv and {contents}"
    )
    
    # Collect all messages from the group chat
    all_messages = []
    for message in groupchat.messages:
        if isinstance(message, dict) and 'content' in message:
            all_messages.append(f"{message.get('name', 'Unknown')}: {message['content']}")
        elif isinstance(message, tuple) and len(message) == 2:
            agent, content = message
            all_messages.append(f"{agent.name}: {content}")
        else:
            all_messages.append(str(message))
    
    # Join all messages into a single string
    response = "\n".join(all_messages)
    
    # Check if a plot was generated
    plot_path = "groupchat/TSLA_Volatility.png"
    if os.path.exists(plot_path):
        # Read the image file
        with open(plot_path, "rb") as img_file:
            img_bytes = img_file.read()
        
        # Create a PIL Image object
        img = Image.open(io.BytesIO(img_bytes))
        
        # Convert PIL Image to Panel Image
        panel_img = pn.pane.Image(img)
        
        # Add the image to the chat interface
        instance.stream(panel_img, user="System")
    
    return response

chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send(
    "What would you like to do? ",
    user="System",
    respond=False,
)
chat_interface.servable()

#  analyze Tesla stock data and generate a volatility plot.