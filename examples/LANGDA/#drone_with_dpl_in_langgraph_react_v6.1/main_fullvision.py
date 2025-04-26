import os
import time

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph

from state import BasicState
from config import paths
from utils import _draw_mermaid_png
from agent import GenerateNodes, EvaluateNodes, GeneralNodes
# from tools_v1 import CustomTestTool, CustomSearchTool, CustomTrainTool
"""
Full vision means that LLM processes the complete prompt uniformly and generates all code content at the same time.
"""
class Langda_Agent(object):
    def __init__(self, rule_string:str, model_name, 
                addition_input:dict={
                     "prefix":"",
                     "user_context":"",
                     "error_report":"",
                     "config":{"configurable": {"thread_id": "2"}}
                },
                caching:bool=False, saving:bool=False):
        # self.rule_string, self.requirements_list = self._parse(rule_string)
        self.generate_prompt:str = paths.load_prompt("generate")
        self.evaluate_prompt:str = paths.load_prompt("evaluate")
        self.regenerate_prompt:str = paths.load_prompt("regenerate")

        # User inputs:
        self.state = BasicState()
        self.state["config"] = addition_input["config"]
        self.state["prefix"] = addition_input["prefix"]
        self.state["model_name"] = model_name
        self.state["rule_string"] = rule_string
        self.state["user_context"] = addition_input["user_context"]

        # Prompting static parameters:
        self.state["tools"] = [
                # CustomTestTool(),
            ]
        self.state["placeholder"] = "{{LANGDA}}"
        self.state["error_report"] = addition_input["error_report"]

        self.checkpointer = MemorySaver()

    #######################################################################################
    ###                                      TEST                                       ###
    #######################################################################################
    def call_langda_workflow(self):
        self.state["srttime"] = time.time()
        self.state["iter_count"] = 0

        langda_workflow = StateGraph(BasicState)
        langda_workflow.set_entry_point("init_node")
        langda_workflow.add_node("init_node", GeneralNodes.init_node)
        langda_workflow.add_node("generate_node", GenerateNodes.generate_node)
        langda_workflow.add_node("test_node", EvaluateNodes.test_node)
        langda_workflow.add_node("summary_node", GeneralNodes.summary_node)

        langda_workflow.add_edge(start_key="init_node", end_key='generate_node')
        langda_workflow.add_edge(start_key="generate_node", end_key='test_node')
        langda_workflow.add_conditional_edges("test_node",EvaluateNodes._decide_next, 
            {
                "regenerate_node": "generate_node",
                "summary_node": "summary_node"
            })
        langda_workflow.add_edge(start_key="generate_node", end_key='test_node')
        langda_workflow.set_finish_point("summary_node")

        langda_agent = langda_workflow.compile(checkpointer=self.checkpointer)
        self.state = langda_agent.invoke(self.state, config=self.state["config"])

        _draw_mermaid_png(langda_agent, "langda_agent")


if __name__ == "__main__":
    addition = {}
    addition["user_context"] = """
    please notice distance(X, Y) is a value, so please do not create single clause like: distance(X, bomb) > 10.
    please seen initial_charge, charge_cost and weight as value and use in following form:
    V is value, value < 5 or value > 10...
    """
    rules_string = ""
    rule_path = "/Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/examples/LANGDA/#drone_with_dpl_in_langgraph_v5.4/rules/"
    with open (os.path.join(rule_path,"test/promis_prompt.pl"),"r") as f:
        rules_string += f.read()

    l = Langda_Agent(rules_string, "deepseek-chat")
    l.call_langda_workflow()

