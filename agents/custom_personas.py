from typing import Callable, Dict, Literal, Optional, Union

from autogen.runtime_logging import log_new_agent, logging_enabled

from autogen.agentchat.conversable_agent import ConversableAgent


class CodingAgent(ConversableAgent):
    """(In preview) Assistant agent, designed to solve a task with LLM.

    AssistantAgent is a subclass of ConversableAgent configured with a default system message.
    The default system message is designed to solve a task with LLM,
    including suggesting python code blocks and debugging.
    `human_input_mode` is default to "NEVER"
    and `code_execution_config` is default to False.
    This agent doesn't execute code by default, and expects the user to execute the code.
    """

    DEFAULT_SYSTEM_MESSAGE = """You are a helpful AI coding expert.
    Solve tasks using your coding and language skills.
    In the following cases, suggest python code (in a python coding block), or shell script (in a sh coding block) for the user to execute. You can also suggest R code (in a R coding block) if the task is more on the statistical side.
        1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
        2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
    Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
    When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
    If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
    When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
    Reply "TERMINATE" in the end when everything is done.
    """

    DEFAULT_DESCRIPTION = "A helpful and general-purpose AI assistant that has strong language skills, Python skills, and Linux command line skills."

    def __init__(
        self,
        name: str,
        system_message: Optional[str] = DEFAULT_SYSTEM_MESSAGE,
        llm_config: Optional[Union[Dict, Literal[False]]] = None,
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Literal["ALWAYS", "NEVER", "TERMINATE"] = "NEVER",
        description: Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            name (str): agent name.
            system_message (str): system message for the ChatCompletion inference.
                Please override this attribute if you want to reprogram the agent.
            llm_config (dict or False or None): llm inference configuration.
                Please refer to [OpenAIWrapper.create](/docs/reference/oai/client#create)
                for available options.
            is_termination_msg (function): a function that takes a message in the form of a dictionary
                and returns a boolean value indicating if this received message is a termination message.
                The dict can contain the following keys: "content", "role", "name", "function_call".
            max_consecutive_auto_reply (int): the maximum number of consecutive auto replies.
                default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case).
                The limit only plays a role when human_input_mode is not "ALWAYS".
            **kwargs (dict): Please refer to other kwargs in
                [ConversableAgent](conversable_agent#__init__).
        """
        super().__init__(
            name,
            system_message,
            is_termination_msg,
            max_consecutive_auto_reply,
            human_input_mode,
            llm_config=llm_config,
            description=description,
            **kwargs,
        )
        if logging_enabled():
            log_new_agent(self, locals())

        # Update the provided description if None, and we are using the default system_message,
        # then use the default description.
        if description is None:
            if system_message == self.DEFAULT_SYSTEM_MESSAGE:
                self.description = self.DEFAULT_DESCRIPTION

class PlanningAgent(ConversableAgent):
    """(In preview) Assistant agent, designed to solve a task with LLM.

    AssistantAgent is a subclass of ConversableAgent configured with a default system message.
    The default system message is designed to solve a task with LLM,
    including suggesting python code blocks and debugging.
    `human_input_mode` is default to "NEVER"
    and `code_execution_config` is default to False.
    This agent doesn't execute code by default, and expects the user to execute the code.
    """

    DEFAULT_SYSTEM_MESSAGE = """You are a helpful scientific research planning expert agent with expertise in genomics. Your primary objective is to design comprehensive research plans that address important scientific questions in the field of genomic studies. Your tasks include, but are not necessarily limited to:
    1 - Formulate Research Questions: Analyze a given topic or dataset to generate clear, focused research questions related to genomics, such as gene-disease associations, genomic variation, or evolutionary patterns.
    2 - Define Hypotheses: Develop research hypotheses that are testable and specific, ensuring they align with the research questions. Consider factors like gene expression levels, mutation impacts, and inheritance patterns.
    3 - Suggest Statistical Methods: Recommend appropriate statistical methods for testing the hypotheses. Consider common techniques in genomic research, such as GWAS (Genome-Wide Association Studies), differential gene expression analysis, and population-based studies. Identify the relevant tests (e.g., chi-square, logistic regression, ANOVA) depending on the data and research design.
    4 - Propose Research Design: Lay out a detailed plan, including study design (e.g., cohort, case-control), sample selection, data collection methods (e.g., sequencing techniques), and the timeline of the research project.
    5 - Anticipate Challenges and Solutions: Identify potential challenges in the research process, such as data availability, ethical concerns, or computational limitations, and propose strategies to overcome these challenges.

    Your goal is to provide a step-by-step plan that can be used by researchers to conduct rigorous, reproducible, and insightful genomic studies. Be clear which step uses code, and which step uses your language skill.
    Reply "TERMINATE" in the end when everything is done.
    """

    DEFAULT_DESCRIPTION = "A helpful and general-purpose AI assistant that has strong planning, research, and writing skills."

    def __init__(
        self,
        name: str,
        system_message: Optional[str] = DEFAULT_SYSTEM_MESSAGE,
        llm_config: Optional[Union[Dict, Literal[False]]] = None,
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Literal["ALWAYS", "NEVER", "TERMINATE"] = "NEVER",
        description: Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            name (str): agent name.
            system_message (str): system message for the ChatCompletion inference.
                Please override this attribute if you want to reprogram the agent.
            llm_config (dict or False or None): llm inference configuration.
                Please refer to [OpenAIWrapper.create](/docs/reference/oai/client#create)
                for available options.
            is_termination_msg (function): a function that takes a message in the form of a dictionary
                and returns a boolean value indicating if this received message is a termination message.
                The dict can contain the following keys: "content", "role", "name", "function_call".
            max_consecutive_auto_reply (int): the maximum number of consecutive auto replies.
                default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case).
                The limit only plays a role when human_input_mode is not "ALWAYS".
            **kwargs (dict): Please refer to other kwargs in
                [ConversableAgent](conversable_agent#__init__).
        """
        super().__init__(
            name,
            system_message,
            is_termination_msg,
            max_consecutive_auto_reply,
            human_input_mode,
            llm_config=llm_config,
            description=description,
            **kwargs,
        )
        if logging_enabled():
            log_new_agent(self, locals())

        # Update the provided description if None, and we are using the default system_message,
        # then use the default description.
        if description is None:
            if system_message == self.DEFAULT_SYSTEM_MESSAGE:
                self.description = self.DEFAULT_DESCRIPTION

class StatisticsAgent(ConversableAgent):
    """(In preview) Assistant agent, designed to solve a task with LLM.

    AssistantAgent is a subclass of ConversableAgent configured with a default system message.
    The default system message is designed to solve a task with LLM,
    including suggesting python code blocks and debugging.
    `human_input_mode` is default to "NEVER"
    and `code_execution_config` is default to False.
    This agent doesn't execute code by default, and expects the user to execute the code.
    """

    DEFAULT_SYSTEM_MESSAGE = """You are a helpful AI statistical analysis expert agent responsible for developing and executing a statistical plan based on predefined research hypotheses. Your tasks include:
    1 - Formulate Statistical Hypotheses: For each research hypothesis, define the corresponding null and alternative statistical hypotheses. Ensure that they are clear, specific, and testable (e.g., null hypothesis: no association between a gene variant and a disease).
    2 - Select Appropriate Statistical Tests: Based on the nature of the data (e.g., continuous, categorical, binary) and the research design (e.g., case-control, cohort, time series), recommend the most suitable statistical tests. Examples might include t-tests, chi-square tests, ANOVA, logistic regression, or non-parametric tests if necessary.
    3 - Verify Statistical Assumptions: Assess whether the data meet the assumptions required for each selected test (e.g., normality, homoscedasticity, independence). If assumptions are violated, suggest appropriate transformations or alternative tests (e.g., using non-parametric methods, data normalization, or robust statistical techniques).
    4 - Perform Power Analysis (if applicable): If sample size is a concern, conduct a power analysis to determine the likelihood of detecting a statistically significant effect given the sample size and effect size. Adjust recommendations accordingly if more data are needed.
    5 - Execute the Statistical Tests: Conduct the selected statistical analyses, ensuring the correct implementation of the tests and calculation of p-values and confidence intervals.
    6 - Interpret the Results: Provide a statistical interpretation of the results, considering a significance level (α) of 0.05. Explain the meaning of the p-value in the context of the null hypothesis and determine whether the results are statistically significant. Also, interpret effect sizes and any relevant measures of association (e.g., odds ratios, correlation coefficients).
    7 - Report Findings: Summarize the statistical findings in a clear and actionable format, highlighting whether the results support or refute the research hypotheses. Include any caveats regarding limitations or assumptions that may impact the interpretation of the results.
    Your goal is to produce a robust statistical analysis plan and provide clear interpretations of the results that can be used to make informed decisions in genomic research.
    Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
    When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
    If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
    When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
    Reply "TERMINATE" in the end when everything is done.
    """

    DEFAULT_DESCRIPTION = "A helpful and general-purpose AI assistant that has strong language skills, statistical skills, and Python and R code skills."

    def __init__(
        self,
        name: str,
        system_message: Optional[str] = DEFAULT_SYSTEM_MESSAGE,
        llm_config: Optional[Union[Dict, Literal[False]]] = None,
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Literal["ALWAYS", "NEVER", "TERMINATE"] = "NEVER",
        description: Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            name (str): agent name.
            system_message (str): system message for the ChatCompletion inference.
                Please override this attribute if you want to reprogram the agent.
            llm_config (dict or False or None): llm inference configuration.
                Please refer to [OpenAIWrapper.create](/docs/reference/oai/client#create)
                for available options.
            is_termination_msg (function): a function that takes a message in the form of a dictionary
                and returns a boolean value indicating if this received message is a termination message.
                The dict can contain the following keys: "content", "role", "name", "function_call".
            max_consecutive_auto_reply (int): the maximum number of consecutive auto replies.
                default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case).
                The limit only plays a role when human_input_mode is not "ALWAYS".
            **kwargs (dict): Please refer to other kwargs in
                [ConversableAgent](conversable_agent#__init__).
        """
        super().__init__(
            name,
            system_message,
            is_termination_msg,
            max_consecutive_auto_reply,
            human_input_mode,
            llm_config=llm_config,
            description=description,
            **kwargs,
        )
        if logging_enabled():
            log_new_agent(self, locals())

        # Update the provided description if None, and we are using the default system_message,
        # then use the default description.
        if description is None:
            if system_message == self.DEFAULT_SYSTEM_MESSAGE:
                self.description = self.DEFAULT_DESCRIPTION
