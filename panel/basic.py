import autogen
# Define configurations for AutoGen
config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4"],
    },
)




#### DEFINE AGENTS 

llm_config = {"config_list": config_list_gpt4, "seed": 42,"api_type": "openai"}

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
    name="Coder",  # the default assistant agent is capable of solving problems with code
    llm_config=llm_config,
)
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="""Critic. You are a helpful assistant highly skilled in evaluating the quality of a given financial visualization code by providing a score from 1 (bad) - 10 (good) while providing clear rationale...
{see full system message above}
""",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)


# START 
user_proxy.initiate_chat(manager, message="Download data from /Users/ai/Documents/sundai/automated-data-scientist/panel/TSLA.csv and show me a plot that tells me about daily volatility. Save the plot to a file. Print the fields in a dataset before visualizing it. Take the feedback from the critic to improve the code.")
