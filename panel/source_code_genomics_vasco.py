import panel as pn
import autogen
import os
import io
from PIL import Image
import sys 
from agents.custom_personas import PlanningAgent
from tools.rag_engine import rag_query


css = """
:root {
    --design-primary-color: #a9a9a9; /* Neon Grey */
    --design-secondary-color: #2f2f2f; /* Dark Grey Neon */
    --design-background-color: #121212; /* Dark Background */
    --design-text-color: #333333; /* Darker text color for better readability */
    font-family: 'Roboto', sans-serif;

}

body {
    background-image: url('panel/background_automated_ai_genomic_data_scientis_dark_backround.png');
    background-color: #121212; /* Fallback color in case the image fails to load */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-color: rgba(15, 12, 41, 0.85); /* Dark overlay */
}

.chat-container {
    background-color: rgba(30, 30, 47, 0.5); /* Semi-transparent background for the chat area */
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    padding: 20px;
    margin: 10px;
}

.message {
    background: rgba(255, 255, 255, 0.5); /* White background with 50% transparency */
    color: var(--design-text-color);
    padding: 10px 20px;
    border-radius: 10px;
    margin-bottom: 8px;
    opacity: 0.5; /* 50% transparency */
}

.timestamp {
    color: #ffffff; /* White text color */
}

.icon, .bk-TablerIcon {
    color: #ffffff; /* White text color */
}

input, button {
    background: linear-gradient(to right, var(--design-primary-color), var(--design-secondary-color));
    color: white;
    padding: 10px 20px;
    border-radius: 20px;
    border: none;
    transition: background-color 0.3s, transform 0.2s;
}

button:hover {
    background-color: var(--design-secondary-color);
    transform: scale(1.05);
}

input[type='text'], textarea {
    background: linear-gradient(to right, #000, #999); /* Gradient background for input fields */
    color: white;
    border: none;
    opacity: 0.5; /* 50% transparency */
    padding: 8px;
    border-radius: 10px;
}
"""

# # Apply the global CSS to the Panel extension
pn.extension(raw_css=[css])
# pn.extension(design="material")

# Define configurations for AutoGen
config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4o-mini"],
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
    system_message="""Critic. You are a helpful assistant highly skilled in evaluating the quality of a given visualization code for genomic data by providing a score from 1 (bad) - 10 (good) while providing clear rationale...""",
    llm_config=llm_config,
)
planner = PlanningAgent(
    name="Planner",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, planner, coder, critic], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    # RAG on the message
    rag_knowledge = rag_query(contents, knowledge_sources_dir='knowledge_sources')
    # Use AutoGen to process the message
    user_proxy.initiate_chat(
        manager,
        message=f"Download data from /Users/vprudente/Downloads/automated_data_scientist/panel/homo_sapiens_genomics.csv and {contents}. Use as inspiration the following knowledge {rag_knowledge}"
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

# analyze this genomic data and plot Distribution of features across chromosomes: Create a stacked bar chart showing the count of different features (e.g., genes, exons, transcripts) for each chromosome (seqname).
