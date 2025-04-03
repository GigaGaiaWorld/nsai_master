from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Dict, Any

from typing import TypedDict, List, Dict, Any, Optional
from enum import Enum

class TaskStatus(str, Enum):
    INIT = "init" # Initial state

    CONTEXT_ANALYSIS = "context_analysis" # Analyze the context of user input

    CODE_GENERATION = "code_generation" # Generate new code

    CODE_TESTING = "code_testing" # Test the newly generated code

    FEEDBACK_ANALYSIS = "feedback_analysis" # Analyze test feedback

    COMPLETED = "completed" # Task completed

    FAILED = "failed" # Task failed


class BasicState(TypedDict):
    # Basic information
    status: TaskStatus # Current task status
    net_structure: List[tuple]
    iter_count: int # Current number of iterations

    # Original input
    rule_string: str # User-provided context
    user_context: str # User-provided context

    # Generated Content
    prompt_rule_template: str
    prompt_rule_requirements: List[str]
    generated_codes: Optional[list] # New code generated
    generated_new_ruleset: str # New code generated


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