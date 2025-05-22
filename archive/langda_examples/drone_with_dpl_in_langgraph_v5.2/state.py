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

    CONTEXT_ANALYSIS = "context_analysis" # Analyze the context of user input

    CODE_GENERATION = "code_generation" # Generate new code

    CODE_TESTING = "code_testing" # Test the newly generated code

    FEEDBACK_ANALYSIS = "feedback_analysis" # Analyze test feedback

    COMPLETED = "completed" # Task completed

    FAILED = "failed" # Task failed

class Mode(str, Enum):
    PURE_PARAM = "normal" # langda(X:"str"), langda(X,Y,...), langda():no parameter

    PURE_NET = "pure net" # langda(NET:"[mnist_net1(0,1), mnist_net2(2,3)]")

    PURE_LLM = "pure llm" # langda(LLM:"str")

    LLM_WITH_RETURN = "llm with return" # langda(X:"str",LLM:"str...") # the answer will stored in parameter and return as aprameter

    # langda(X:"return", T:"time", NET:"[mnist_net1(0,1), mnist_net2(2,3)], LLM:"str...") # 
    # langda(X:"str", NET:"[mnist_net1(0,1)]") # call llm with no description -> # PARAM_WITH_NET
    FULL_PART = "full part" 

    ELSE = "else case" # langda(NET:[net(0,1)],LLM:"")


class BasicState(TypedDict):
    # Basic information
    status: TaskStatus # Current task status
    mode: Mode # Which mode to choose for langda
    net_structure: List[tuple]
    iter_count: int # Current number of iterations

    # Original input
    rule_string: str # User-provided context
    user_context: str # User-provided context

    # Generated Content
    prompt_rule_template: str # the string that only leave "{LLM}" slot for prompting
    prompt_rule_dict: List[str] # the dict that contains detail informations
    prompt_requirements: str # Prompt part reconstructed from prompt_rule_dict
    generated_new_codes: str # New code generated
    generated_new_ruleset: str # New


    user_feedback: str # User-provided feedback about the result
    test_results: Optional[Dict[str, Any]] # Test results


    # Tool status
    # retrieved_docs: Optional[List[Dict[str, Any]]] # Retrieved documents


# 创建一个记忆管理类
class MemoryManager:
    def __init__(self):
        self.memory = ConversationBufferMemory(return_messages=True)
    
    def load_memory(self, state: BasicState) -> BasicState:
        """load memory to current state"""
        if "chat_history" in state["memory"]:
            for message in state["memory"]["chat_history"]:
                if message["type"] == "human":
                    self.memory.chat_memory.add_user_message(message["content"])
                elif message["type"] == "ai":
                    self.memory.chat_memory.add_ai_message(message["content"])
        return state
    
    def save_memory(self, state: BasicState) -> BasicState:
        """save current state to memory"""

        if state["messages"]:
            last_message = state["messages"][-1]
            if last_message["type"] == "human":
                self.memory.chat_memory.add_user_message(last_message["content"])
            elif last_message["type"] == "ai":
                self.memory.chat_memory.add_ai_message(last_message["content"])

        state["memory"]["chat_history"] = [
            {"type": "human" if isinstance(msg, HumanMessage) else "ai", "content": msg.content}
            for msg in self.memory.chat_memory.messages
        ]
        return state