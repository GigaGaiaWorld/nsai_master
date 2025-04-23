from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Dict, Any

from typing import TypedDict, List, Dict, Any, Optional
from enum import Enum

class LangdaItem(Dict[str, str]): ...
class FullLangdaDict(TypedDict):
    Block: List[str]
    Head: str
    Langda: List[LangdaItem]

class TaskStatus(str, Enum):
    INIT = "init" # Initial state

    GNRT = "code_generating" # Generate new code

    TEST = "code_testing" # Test the newly generated code

    CMPL = "completed" # Task completed

class Mode(str, Enum):
    PURE_PAR = "normal" # langda(X:"str"), langda(X,Y,...), langda():no parameter

    PURE_NET = "pure net" # langda(NET:"[mnist_net1(0,1), mnist_net2(2,3)]")

    PURE_LLM = "pure llm" # langda(LLM:"str")

    PARA_LLM = "llm with actions" # langda(X:"str",LLM:"str...") # the answer will stored in parameter and return as a parameter

    # langda(X:"return", T:"time", NET:"[mnist_net1(0,1), mnist_net2(2,3)], LLM:"str...") # 
    # langda(X:"str", NET:"[mnist_net1(0,1)]") # call llm with no description -> # PARAM_WITH_NET
    FULL_LLM = "full parts" 

    ELSE = "else case" # langda(NET:[net(0,1)],LLM:"")    

class BasicState(TypedDict):
    # Basic information
    srttime: float = 0.0
    endtime: float  = 0.0
    status: TaskStatus # Current task status
    mode: Mode # Which mode to choose for langda
    iter_count: int = 0 # Current number of iterations

    # Original input
    rule_string: str # User-provided context
    user_context: str # User-provided context

    # Generated Content
    prompt_template: str # the string that only leave "{LLM}" slot for prompting
    langda_dicts: List[str] # the dict that contains detail informations about langda
    lann_dicts: List[str] # the dict that contains detail informations about network
    prompt_requirements: str # Prompt part reconstructed from langda_dicts and lann_dicts
    
    generated_codes: str # New code generated
    evaluated_codes: str # New report generated
    generated_result: str # New
    evaluated_result: str # New
    final_code: str # 

    error_report: str # New report generated
