from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict
from typing_extensions import TypedDict
from enum import Enum
class LangdaDict(TypedDict):
    HEAD: str
    HASH: str

    LOT: str
    NET: str
    LLM: str
    FUP: bool

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
    # User inputs:
    usereact: bool
    config: dict
    prefix: str
    model_name: str
    rule_string: str # User-provided context
    user_context: str # User-provided context
    langda_ext: dict # User-provided context

    # Prompting static parameters:
    tools: list
    has_query: bool
    placeholder: str
    prompt_template: str # the string that only leave "{LLM}" slot for prompting
    langda_dicts: List[LangdaDict] # the dict that contains detail informations about langda
    lann_dicts: List[Dict[str,str]] # the dict that contains detail informations about network
    langda_reqs: str # Prompt part reconstructed from langda_dicts and lann_dicts
    lann_reqs: str # Prompt part reconstructed from langda_dicts and lann_dicts

    # Dynamic parameters:
    srttime: float = 0.0
    endtime: float  = 0.0
    iter_count: int = 0 # Current number of iterations
    status: TaskStatus # Current task status
    fest_codes: List[dict] # The Code that doesn't need further generate
    regenerate_info: str # 
    generated_codes: list # New code generated
    error_report: str # New report generated