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
                     "langda_ext":"",
                     "user_context":"",
                     "error_report":"",
                     "config":{"configurable": {"thread_id": "42"}}
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
        self.state["langda_ext"] = addition_input["langda_ext"]
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

    def call_langda_workflow(self):
        self.state["srttime"] = time.time()
        self.state["iter_count"] = 0

        langda_workflow = StateGraph(BasicState)
        langda_workflow.set_entry_point("init_node")
        langda_workflow.add_node("init_node", GeneralNodes.init_node)
        langda_workflow.add_node("generate_node", GenerateNodes.generate_node)
        langda_workflow.add_node("test_node", EvaluateNodes.test_node)
        langda_workflow.add_node("summary_node", GeneralNodes.summary_node)

        langda_workflow.add_conditional_edges("init_node",GeneralNodes._decide_next_init, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node"
            })
        langda_workflow.add_conditional_edges("generate_node",GenerateNodes._decide_next_gnrt, 
            {
                "generate_node": "generate_node",
                "test_node": "test_node"
            })
        langda_workflow.add_conditional_edges("test_node",EvaluateNodes._decide_next_eval, 
            {
                "generate_node": "generate_node",
                "summary_node": "summary_node"
            })
        langda_workflow.set_finish_point("summary_node")

        langda_agent = langda_workflow.compile(checkpointer=self.checkpointer)
        self.state = langda_agent.invoke(self.state, config=self.state["config"])

        _draw_mermaid_png(langda_agent, "langda_agent")

if __name__ == "__main__":
    def process_all_prompt_files(directory_path, model_name, addition_input):  
        # Find all files ending with "prompt.pl"
        prompt_files = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith("prompt.pl"):
                    prompt_files.append(os.path.join(root, file))
        
        # Process each prompt file
        for prompt_file in prompt_files:
            print(f"#=================Processing file: {prompt_file} =================#")

            # Extract prefix from filename (remove _prompt.pl suffix)
            file_basename = os.path.basename(prompt_file)
            prefix = file_basename.replace("_prompt.pl", "")

            # Update the prefix in addition_input
            file_specific_input = addition_input.copy()
            file_specific_input["prefix"] = prefix

            # Read the rules from the file
            with open(prompt_file, "r") as f:
                rules_string = f.read()

            # Create and run the agent
            agent = Langda_Agent(rules_string, model_name, addition_input=file_specific_input)
            agent.call_langda_workflow()

            print(f"#=================Completed processing: {prompt_file} =================#")

    def combine_results(directory_path):
        print("in combine_results")
        # Find all files ending with "result.txt"
        result_files = []  # Changed variable name from prompt_files to result_files
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith("result.txt"):
                    result_files.append(os.path.join(root, file))
        # Process each result file
        for result_file in result_files:  # Changed variable name from prompt_file to result_file
            print("result_file",result_file)
            file_basename = os.path.basename(result_file)

            with open(result_file, "r") as f:  # Changed from prompt_file to result_file
                result = f.read()

            with open(f"{directory_path}/gathered_final_result.txt", "a") as f:
                f.write(f"\n\n=============={file_basename}:==============\n")
                f.write(result)
    
    addition = {
        "prefix": "",  # Will be updated for each file
        "langda_ext": msg_from_bot,  # Will be updated for each file
        "error_report": "",
        "config": {"configurable": {"thread_id": "42"}},
        "user_context": ""
    }
    test_path = paths.get_abscase_path("rules/test")
    final_path = paths.get_abscase_path("history/final")
    # process_all_prompt_files(test_path, "deepseek-chat", addition) 
    combine_results(final_path)