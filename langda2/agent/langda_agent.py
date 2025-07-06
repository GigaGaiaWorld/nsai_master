import time
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph

from .state import BasicState
from .generate_nodes import GenerateNodes
from .evaluate_nodes import EvaluateNodes
from .general_nodes import GeneralNodes
from pathlib import Path
from uuid import uuid4
from ..config import paths

def _draw_mermaid_png(graph: StateGraph, graph_str: str):
    """Generate mermaid file for the graph visualization"""
    graph_mermaid = graph.get_graph().draw_mermaid()
    paths.save_as_file(graph_mermaid, "mermaid", graph_str)

class LangdaAgentBase:
    """Base class for all Langda agents with common initialization"""
    
    def __init__(self, rule_string, model_name, addition_input: dict = None):
        self.state = BasicState()
        
        # User inputs
        self.state["model_name"] = model_name
        self.state["rule_string"] = rule_string
        self.state["final_result"] = ""
        
        # Additional input configuration
        if addition_input is None:
            addition_input = {}
        
        self.state["config"] = addition_input.get("config", 
        {
            "configurable": {
                "thread_id": str(uuid4),       # ID
                "checkpoint_ns": "langda",       # namespace
                "checkpoint_id": None,           # checkpoint ID
            }
        })
        self.state["prefix"] = addition_input.get("prefix") or "main"
        self.state["load"] = addition_input.get("load")
        self.state["langda_ext"] = addition_input.get("langda_ext")
        self.state["query_ext"] = addition_input.get("query_ext")
        self.state["save_dir"] = addition_input.get("save_dir") or Path(paths.base_dir) / "history"
        self.state["build_dir"] = addition_input.get("build_dir") or Path(paths.base_dir) / "build"

        # Initialize test analysis with syntax notes
        self.state["test_analysis"] = []
        with open(Path(__file__).parent.parent / "prompts"/ "Problog_Syntax.txt", "r") as f_s:
            self.state["test_analysis"].append(f_s.read())
        
        # Static parameters
        self.state["tools"] = ["retriever_tool", "search_tool"]
        self.state["placeholder"] = "{{LANGDA}}"
        
        self.checkpointer = MemorySaver()

    def _create_workflow(self, workflow_type: str) -> StateGraph:
        """Create workflow based on type"""
        self.state["srttime"] = time.time()
        self.state["iter_count"] = 0
        
        workflow = StateGraph(BasicState)
        workflow.set_entry_point("init_node")
        workflow.add_node("init_node", GeneralNodes.init_node)
        workflow.add_node("generate_node", GenerateNodes.generate_node)
        workflow.add_node("summary_node", GeneralNodes.summary_node)
        workflow.add_node("test_node", EvaluateNodes.test_node)
        # Add conditional edges from init_node
        workflow.add_conditional_edges("init_node", GeneralNodes._decide_next_init, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node",
            })
        
        if workflow_type == "single":
            # Simple workflow: generate -> summary
            workflow.add_edge("generate_node", "summary_node")
        else:
            # Double workflow: generate -> test -> generate/summary
            workflow.add_conditional_edges("generate_node", GenerateNodes._decide_next_gnrt, 
                {
                    "generate_node": "generate_node",
                    "test_node": "test_node"
                })
            workflow.add_conditional_edges("test_node", EvaluateNodes._decide_next_eval, 
                {
                    "generate_node": "generate_node",
                    "summary_node": "summary_node"
                })
        
        workflow.set_finish_point("summary_node")
        return workflow

    def call_langda_workflow(self) -> dict:
        """Execute the workflow and return results"""
        workflow_type = "double" if "evaluate" in self.state["agent_type"] else "single"
        langda_workflow = self._create_workflow(workflow_type)
        
        langda_agent = langda_workflow.compile(checkpointer=self.checkpointer)
        self.state = langda_agent.invoke(self.state, config=self.state["config"])
        
        graph_name = f"langda_agent_{workflow_type}"
        _draw_mermaid_png(langda_agent, graph_name)
        
        return self.state["final_result"]

# Specific agent implementations
class LangdaAgentSingleSimple(LangdaAgentBase):
    """Single workflow with simple agent"""
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        self.state["agent_type"] = {"generate": "simple"}

class LangdaAgentSingleReact(LangdaAgentBase):
    """Single workflow with react agent"""
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        self.state["agent_type"] = {"generate": "react"}

class LangdaAgentSingleDC(LangdaAgentBase):
    """Single workflow with doublechain agent"""
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        self.state["agent_type"] = {"generate": "doublechain"}

class LangdaAgentDoubleSimple(LangdaAgentBase):
    """Double workflow with simple agents"""
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        self.state["agent_type"] = {
            "generate": "simple",
            "evaluate": "simple"
        }

class LangdaAgentDoubleReact(LangdaAgentBase):
    """Double workflow with react agents"""
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        self.state["agent_type"] = {
            "generate": "react",
            "evaluate": "react"
        }

class LangdaAgentDoubleDC(LangdaAgentBase):
    """Double workflow with doublechain agents"""
    def __init__(self, rule_string, model_name, addition_input=None):
        super().__init__(rule_string, model_name, addition_input)
        self.state["agent_type"] = {
            "generate": "doublechain",
            "evaluate": "doublechain"
        }