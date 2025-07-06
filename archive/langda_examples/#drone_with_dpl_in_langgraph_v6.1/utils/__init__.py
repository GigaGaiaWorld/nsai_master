# utils/__init__.py
from typing import Union
from .models import LangdaAgentExecutor
from .parser import integrated_code_parser
from .tools import (
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

__all__ = [
    'invoke_agent',
    '_compute_short_md5',
    '_compute_random_md5',
    '_list_to_dict',
    '_langda_list_to_dict',
    '_expand_nested_list',
    '_parse_simple_dictonary',
    'integrated_code_parser',
    '_ordinal',
    '_find_all_blocks',
    '_draw_mermaid_png',
    '_replace_placeholder'
]

def invoke_agent(react: bool, model_name: str, tools: list, prompt_type, input, config) -> tuple[str,str]:
    """
    Returns the corresponding LangdaAgentExecutor instance or its react version based on the parameters passed in when calling.
    Args:
        react: Use react agent?
        model_name: name of llm model
        prompt_type: One of ["evaluate", "generate", "regenerate"]
        input: dictonary to fill all the placeholders in prompt
        config: configs of agent for example: {"configurable": {"thread_id": "2"}}
    """
    executor = LangdaAgentExecutor(model_name, tools)
    if react:
        return executor.invoke_react_agent(prompt_type,input,config)
    else:
        return executor.invoke_agent(prompt_type,input,config)
