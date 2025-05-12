# utils/__init__.py
import inspect
from typing import Union, List, Literal
from langchain.tools import BaseTool
from .models import LangdaAgentExecutor
from .parser_v2 import integrated_code_parser
from .format_tools import (
    _ordinal,
    _list_to_dict, 
    _expand_nested_list,
    _draw_mermaid_png, 
    _replace_placeholder, 
    _find_all_blocks, 
    _compute_short_md5, 
    _compute_random_md5, 
    _parse_simple_dictonary, 
    _langda_list_to_dict,
)
from .agent_tools import TOOL_REGISTRY
__all__ = [
    'invoke_agent',
    'get_tools',

    '_ordinal',
    '_list_to_dict',
    '_compute_short_md5',
    '_compute_random_md5',
    '_langda_list_to_dict',
    '_expand_nested_list',
    '_parse_simple_dictonary',
    'integrated_code_parser',
    '_find_all_blocks',
    '_draw_mermaid_png',
    '_replace_placeholder',
]

def invoke_agent(react:bool, model_name:str, tools:List[str], prompt_type:Literal["evaluate", "generate", "regenerate"], input:dict, config:dict) -> tuple[str,str]:
    """
    Returns the corresponding LangdaAgentExecutor instance or its react version based on the parameters passed in when calling.
    Args:
        react: Use react agent?
        model_name: name of llm model
        prompt_type: One of ["evaluate", "generate", "regenerate"]
        input: dictonary to fill all the placeholders in prompt
        config: configs of agent for example: {"configurable": {"thread_id": "2"}}
    """
    executor = LangdaAgentExecutor(model_name=model_name,tools=get_tools(tools))
    if react:
        return executor.invoke_react_agent(prompt_type,input,config)
    else:
        return executor.invoke_agent(prompt_type,input,config)

def get_tools(tool_list: List[str]) -> List[BaseTool]:
    """
    Get tool instances based on the list of tool names.
    args:
        tool_list: List of tool names to load, currently we have "search_tool", "retriever_tool", "problog_test_tool"
    returns:
        List of instantiated tool objects
    """
    tools = []
    
    for tool_name in tool_list:
        entry = TOOL_REGISTRY.get(tool_name)
        if entry is None:
            print(f"Warning: Tool '{tool_name}' not found")
            continue
        if inspect.isclass(entry) and issubclass(entry,BaseTool): # if is class -> Instantiate
            tools.append(entry())
        elif isinstance(entry,BaseTool): # if already Instantiated
            tools.append(entry)
        else:
            print(f"Warning: Tool '{tool_name}' not found in registry")

    return tools