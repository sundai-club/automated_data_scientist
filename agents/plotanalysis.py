import os
from llm_config import llm_config
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
import json
import random
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import matplotlib.pyplot as plt
import numpy as np
import requests
from PIL import Image
from termcolor import colored

import autogen
from autogen import Agent, AssistantAgent, ConversableAgent, UserProxyAgent
from autogen.agentchat.contrib.capabilities.vision_capability import VisionCapability
from autogen.agentchat.contrib.img_utils import get_pil_image, pil_to_data_uri
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from autogen.code_utils import content_str

config_list_4v = [
    {"model": "gpt-4o","api_key": "",}
]


config_list_gpt4 = [{"model": "gpt-4o-mini","api_key": "",}]

gpt4_llm_config = {"config_list": config_list_gpt4, "cache_seed": 42}

image_agent = MultimodalConversableAgent(
    name="image-explainer",
    max_consecutive_auto_reply=10,
    llm_config={"config_list": config_list_4v, "temperature": 0.5, "max_tokens": 300},
)

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="You are an expert Data Scientist, your goal is to analyze the given plot to infer what it is showing. \
        The input is given as \"Description_Message IMAGE_ADDRESS\". \
        So you also need to evaluate that the plot matches the what's expected in the description message. If it doesn't make sure to point that out.\
        As an expert data scientist you should provide detailed qualitative and quantitative analysis of the plot and also suggest any improvements \
        that can be done to address the given description better or generally.",
    human_input_mode="NEVER",  # Try between ALWAYS or NEVER
    max_consecutive_auto_reply=0,
    code_execution_config={
        "use_docker": False
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)

