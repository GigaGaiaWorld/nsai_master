import time
from typing import Protocol, Dict, Any, Optional
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END

from .state import BasicState
from .generate_nodes import GenerateNodes
from .evaluate_nodes import EvaluateNodes
from .general_nodes import GeneralNodes
from ..config import paths

def _draw_mermaid_png(graph:StateGraph, graph_str:str):
    """
    well, it will not give you the mermaid_png because of the restrict of api,
    But it will generate a mmd file, you can generate png yourself from https://mermaid.live/edit
    args:
        graph: current StateGraph
        graph_str: name of the graph, only used for creating filename
    """
    graph_mermaid = graph.get_graph().draw_mermaid()
    paths.save_as_file(graph_mermaid,"mermaid", graph_str)

class LangdaAgentProtocol(Protocol):
    """
    The interface protocol of LangdaAgent.
    """
    
    def __init__(self, 
                rule_string: str, 
                model_name: str, 
                addition_input: Optional[Dict[str, Any]] = None) -> None:
        ...
    
    def call_langda_workflow(self) -> Dict[str, Any]:
        ...


class LangdaAgentBase:
    """Base class for all Langda agents with common initialization"""
    
    def __init__(self, rule_string, model_name, addition_input:dict=None):
        
        self.state = BasicState()
        # User inputs
        self.state["model_name"] = model_name
        self.state["rule_string"] = rule_string
        self.state["final_result"] = ""
        # addition_input:
        self.state["config"] = addition_input.get("config", {"configurable": {"thread_id": "42"}})
        self.state["prefix"] = addition_input.get("prefix", "main")
        self.state["load"] = addition_input.get("load", False)
        self.state["langda_ext"] = addition_input.get("langda_ext", "")
        self.state["query_ext"] = addition_input.get("query_ext", "")

        self.state["test_analysis"] = []
        with open(paths.get_abscase_path("prompts/Problog_Syntax.txt"), "r") as f_s:
            self.state["test_analysis"].append(f_s.read())
        # Prompting static parameters
        self.state["tools"] = ["retriever_tool","search_tool"]

        self.state["placeholder"] = "{{LANGDA}}"

        self.checkpointer = MemorySaver()

    def call_langda_workflow(self) -> dict:
        pass

class LangdaAgentSingleSimple(LangdaAgentBase):
    """Simple Langda workflow with a simple agent"""
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        # Set agent type information for this specific agent type
        self.state["agent_type"] = {
            "generate": "simple",
        }

    def call_langda_workflow(self) -> dict:
        self.state["srttime"] = time.time()
        self.state["iter_count"] = 0
        langda_workflow = StateGraph(BasicState)
        langda_workflow.set_entry_point("init_node")
        langda_workflow.add_node("init_node", GeneralNodes.init_node)
        langda_workflow.add_node("generate_node", GenerateNodes.generate_node)
        langda_workflow.add_node("summary_node", GeneralNodes.summary_node)

        langda_workflow.add_conditional_edges("init_node", GeneralNodes._decide_next_init, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node",
                "END": END
            })
        langda_workflow.add_edge("generate_node", "summary_node")
        langda_workflow.set_finish_point("summary_node")
        
        langda_agent = langda_workflow.compile(checkpointer=self.checkpointer)
        self.state = langda_agent.invoke(self.state, config=self.state["config"])
        
        _draw_mermaid_png(langda_agent, "langda_agent_simple")
        
        return self.state["final_result"]

class LangdaAgentSingleDC(LangdaAgentBase):
    """Simple Langda workflow with a simple agent"""
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        # Set agent type information for this specific agent type
        self.state["agent_type"] = {
            "generate": "doublechain",
        }

    def call_langda_workflow(self) -> dict:
        self.state["srttime"] = time.time()
        self.state["iter_count"] = 0
        langda_workflow = StateGraph(BasicState)
        langda_workflow.set_entry_point("init_node")
        langda_workflow.add_node("init_node", GeneralNodes.init_node)
        langda_workflow.add_node("generate_node", GenerateNodes.generate_node)
        langda_workflow.add_node("summary_node", GeneralNodes.summary_node)


        langda_workflow.add_conditional_edges("init_node", GeneralNodes._decide_next_init, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node",
                "END": END
            })
        langda_workflow.add_edge("generate_node", "summary_node")
        langda_workflow.set_finish_point("summary_node")
        
        langda_agent = langda_workflow.compile(checkpointer=self.checkpointer)
        self.state = langda_agent.invoke(self.state, config=self.state["config"])
        
        _draw_mermaid_png(langda_agent, "langda_agent_simple")
        
        return self.state["final_result"]

    
class LangdaAgentDoubleDC(LangdaAgentBase):
    """
        "generate": "doublechain",
        "evaluate": "doublechain"
    """
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        # Set agent type information for this specific agent type
        self.state["agent_type"] = {
            "generate": "doublechain",
            "evaluate": "doublechain"
        }
    def call_langda_workflow(self) -> dict:
        self.state["srttime"] = time.time()
        self.state["iter_count"] = 0

        langda_workflow = StateGraph(BasicState)
        langda_workflow.set_entry_point("init_node")
        langda_workflow.add_node("init_node", GeneralNodes.init_node)
        langda_workflow.add_node("generate_node", GenerateNodes.generate_node)
        langda_workflow.add_node("test_node", EvaluateNodes.test_node)
        langda_workflow.add_node("summary_node", GeneralNodes.summary_node)

        langda_workflow.add_conditional_edges("init_node", GeneralNodes._decide_next_init, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node",
                "END": END
            })
        langda_workflow.add_conditional_edges("generate_node", GenerateNodes._decide_next_gnrt, 
            {
                "generate_node": "generate_node",
                "test_node": "test_node"
            })
        langda_workflow.add_conditional_edges("test_node", EvaluateNodes._decide_next_eval, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node"
            })
        langda_workflow.set_finish_point("summary_node")

        langda_agent = langda_workflow.compile(checkpointer=self.checkpointer)
        self.state = langda_agent.invoke(self.state, config=self.state["config"])
        
        _draw_mermaid_png(langda_agent, "langda_agent_full")
        
        return self.state["final_result"]

class LangdaAgentDoubleSimple(LangdaAgentBase):
    """Full Langda workflow with simple agent"""
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        # Set agent type information for this specific agent type
        self.state["agent_type"] = {
            "generate": "simple",
            "evaluate": "simple"
        }
    def call_langda_workflow(self) -> dict:
        self.state["srttime"] = time.time()
        self.state["iter_count"] = 0

        langda_workflow = StateGraph(BasicState)
        langda_workflow.set_entry_point("init_node")
        langda_workflow.add_node("init_node", GeneralNodes.init_node)
        langda_workflow.add_node("generate_node", GenerateNodes.generate_node)
        langda_workflow.add_node("test_node", EvaluateNodes.test_node)
        langda_workflow.add_node("summary_node", GeneralNodes.summary_node)

        langda_workflow.add_conditional_edges("init_node", GeneralNodes._decide_next_init, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node",
                "END": END
            })
        langda_workflow.add_conditional_edges("generate_node", GenerateNodes._decide_next_gnrt, 
            {
                "generate_node": "generate_node",
                "test_node": "test_node"
            })
        langda_workflow.add_conditional_edges("test_node", EvaluateNodes._decide_next_eval, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node"
            })
        langda_workflow.set_finish_point("summary_node")

        langda_agent = langda_workflow.compile(checkpointer=self.checkpointer)
        self.state = langda_agent.invoke(self.state, config=self.state["config"])
        
        _draw_mermaid_png(langda_agent, "langda_agent_full")
        
        return self.state["final_result"]


class LangdaAgentDCSimple(LangdaAgentBase):
    """
        "generate": "doublechain",
        "evaluate": "simple"
    """
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        # Set agent type information for this specific agent type
        self.state["agent_type"] = {
            "generate": "doublechain",
            "evaluate": "simple"
        }
    def call_langda_workflow(self) -> dict:
        self.state["srttime"] = time.time()
        self.state["iter_count"] = 0

        langda_workflow = StateGraph(BasicState)
        langda_workflow.set_entry_point("init_node")
        langda_workflow.add_node("init_node", GeneralNodes.init_node)
        langda_workflow.add_node("generate_node", GenerateNodes.generate_node)
        langda_workflow.add_node("test_node", EvaluateNodes.test_node)
        langda_workflow.add_node("summary_node", GeneralNodes.summary_node)

        langda_workflow.add_conditional_edges("init_node", GeneralNodes._decide_next_init, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node",
                "END": END
            })
        langda_workflow.add_conditional_edges("generate_node", GenerateNodes._decide_next_gnrt, 
            {
                "generate_node": "generate_node",
                "test_node": "test_node"
            })
        langda_workflow.add_conditional_edges("test_node", EvaluateNodes._decide_next_eval, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node"
            })
        langda_workflow.set_finish_point("summary_node")

        langda_agent = langda_workflow.compile(checkpointer=self.checkpointer)
        self.state = langda_agent.invoke(self.state, config=self.state["config"])
        
        _draw_mermaid_png(langda_agent, "langda_agent_full")
        
        return self.state["final_result"]