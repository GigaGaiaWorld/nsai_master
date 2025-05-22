from .agent import (
    LangdaAgentSingleSimple,
    LangdaAgentDoubleSimple,
    LangdaAgentDoubleDC,
    LangdaAgentSingleDC,
    LangdaAgentProtocol
)
from typing import Literal
from .utils.parser_v2 import integrated_code_parser

__version__ = "6.5"
__all__ = [
    'langda_solve',
    'integrated_code_parser',
    'LangdaAgentSingleSimple',
    'LangdaAgentDoubleSimple', 
    'LangdaAgentDoubleDC',
    'LangdaAgentSingleDC',
    'LangdaAgentProtocol'
]
def langda_solve(agent_type:Literal["simple", "double", "double_dc", "single_dc"], 
                 rule_string:str, 
                 model_name:str="deepseek-chat", 
                 additional_input:dict={
                    "config":{"configurable": {"thread_id": "42"}}, # session configuration
                    "prefix":"",        # changable prefix, only for differentiate files
                    "langda_ext":{},    # If there's docking content in langda, for example /* Secure */
                }) -> str:
    """
    Create a Langda agent of the specified type.
    Args:
        agent_type: One of "simple", "double", "double_dc", "dc_simple", or "single_dc"
            - simple: language model with improved prompt template, double means 'generate-test-refine loop'
            - double: agent with tools and improved prompt template, double means 'generate-test-refine loop'
        rules_string: The Problog rules to generate code for
        model_name: LLM model to use
        additional_input: about langda_ext
            - you could use langda(LLM:"/* Mark */"). to accept dynamic prompt words as 'port'
            - Then you could give all the dynamic prompts in form of {"Mark":"your real prompt",...}
            - The agent will check all the ports and replace with corresponding prompts
    Returns:
        The executable files created from rules_string
    """
    agent_map = {
        "simple": LangdaAgentSingleSimple,
        "double": LangdaAgentDoubleSimple,
        "double_dc": LangdaAgentDoubleDC,
        "single_dc": LangdaAgentSingleDC,
    }
    
    if agent_type not in agent_map:
        raise ValueError(f"Unknown agent type: {agent_type}. Available types: {list(agent_map.keys())}")
    
    agent_class = agent_map[agent_type]
    agent:LangdaAgentProtocol = agent_class(rule_string, model_name, additional_input)
    result = agent.call_langda_workflow()
    return result['final_result']
