from .agent import (
    LangdaAgentSingleSimple,
    LangdaAgentDoubleSimple,
    LangdaAgentDoubleDC,
    LangdaAgentSingleDC,
    LangdaAgentSingleReact,
    LangdaAgentDoubleReact,
    LangdaAgentProtocol
)
from typing import Literal
from .utils.parser_v2 import integrated_code_parser
from .utils.test_tools import _problog_test
from .utils.format_tools import _find_all_blocks
from .utils import invoke_agent
from uuid import uuid4

__version__ = "6.5"
__all__ = [
    'langda_solve',
    'invoke_agent',

    '_problog_test',
    'integrated_code_parser',
    '_find_all_blocks',

    # As type:
    'LangdaAgentSingleSimple',
    'LangdaAgentDoubleSimple', 
    'LangdaAgentSingleDC',
    'LangdaAgentDoubleDC',
    'LangdaAgentSingleReact',
    'LangdaAgentDoubleReact',
    'LangdaAgentProtocol'
]
def langda_solve(agent_type:Literal["simple", "double", "single_dc", "double_dc", "single_react", "double_react"], 
                 rule_string:str, 
                 model_name:str="deepseek-chat", 

                 config:dict={
                    "configurable": {
                        "thread_id": str(uuid4),       # ID
                        "checkpoint_ns": "langda",       # namespace
                        "checkpoint_id": None,           # checkpoint ID
                    }
                 },
                 prefix:str="",
                 save_dir:str="",
                 load:bool=False,
                 langda_ext:dict={},
                 query_ext:str="",

                #  additional_input:dict={
                #     "config":{"configurable": {"thread_id": "42"}}, # session configuration
                #     "prefix":"",        # changable prefix, only for differentiate files
                #     "load":False,
                #     "langda_ext":{},    # If there's docking content in langda, for example /* Secure */
                #     "query_ext": "",
                # }
) -> str:
    """
    Create a Langda agent of the specified type.
    Args:
        agent_type: One of "simple", "double", "double_dc", "dc_simple", or "single_dc"
            - simple: language model with improved prompt template, double means 'generate-test-refine loop'
            - double: agent with tools and improved prompt template, double means 'generate-test-refine loop'
        rules_string: The Problog rules to generate code for
        model_name: LLM model to use
        additional_input: 
            - config: session configuration
            - prefix: changable prefix, only for differentiate files and database
            - db_root: path to database
            - load: Regardless of whether there is continuously updated code, read directly from database
            - query_ext: for deepproblog file, you need to add facts and query yourself if you want langda test properly.
            - about langda_ext
                1. you could use langda(LLM:"/* Mark */"). to accept dynamic prompt words as 'port'
                2. Then you could give all the dynamic prompts in form of {"Mark":"your real prompt",...}
                3. The agent will check all the ports and replace with corresponding prompts
            
    Returns:
        The executable files created from rules_string
    """
    agent_map = {
        "simple": LangdaAgentSingleSimple,
        "double": LangdaAgentDoubleSimple,
        "single_dc": LangdaAgentSingleDC,
        "double_dc": LangdaAgentDoubleDC,
        "single_react": LangdaAgentSingleReact,
        "double_react": LangdaAgentDoubleReact,
    }
    
    if agent_type not in agent_map:
        raise ValueError(f"Unknown agent type: {agent_type}. Available types: {list(agent_map.keys())}")
    
    agent_class = agent_map[agent_type]

    additional_input:dict={
        "config":config, # session configuration
        "prefix":prefix,        # changable prefix, only for differentiate files
        "save_dir":save_dir,        # changable prefix, only for differentiate files
        "load":load,
        "langda_ext":langda_ext,    # If there's docking content in langda, for example /* Secure */
        "query_ext": query_ext,
    }

    agent:LangdaAgentProtocol = agent_class(rule_string, model_name, additional_input)
    result = agent.call_langda_workflow()
    return result['final_result']
