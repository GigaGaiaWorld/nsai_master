import re
import os
from typing import List
from dotenv import load_dotenv
load_dotenv()
from problog.program import PrologString
from problog import get_evaluatable

# pip install langgraph
from langchain import hub
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import create_react_agent, ToolNode
from langchain_core.output_parsers.string import StrOutputParser

from state import BasicState, TaskStatus
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_deepseek import ChatDeepSeek
from langchain.tools import BaseTool

import config as cf
from tools_v1 import CustomTestTool, CustomSearchTool, CustomTrainTool

class Langda_Agent(object):
    def __init__(self, rule_string:str, addition_input:dict={"user_context":"..."}, caching:bool=False, saving:bool=False):
        # self.rule_string, self.requirements_list = self._parse(rule_string)
        self.generated_codes = list()
        self.prompt_template:str = cf.SYSTEM_PROMPT_FORMAT_LANGDA
        self.state = BasicState()
        self.state["user_context"] = addition_input["user_context"]
        self.state["rule_string"] = rule_string
        self.config = {"configurable": {"thread_id": "2"}}
        self.checkpointer = MemorySaver()

        self.path_to_rule = cf.GENERATED_RULE_PATH
        self.model=ChatDeepSeek(
            model="deepseek-chat", 
            temperature=0,
            api_key="sk-293f9d735260457583c3cbe0df475d4f")
        self.tools = [
                CustomTestTool(),
            ]


    def _construct_prompt(self) -> ChatPromptTemplate:

        return ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that helps the user to generate deepproblog code."),
            ("human", self.prompt_template)
        ])

    def _draw_mermaid_png(self,graph:StateGraph, graph_str:str):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        graph_mermaid = graph.get_graph().draw_mermaid()
        with open(os.path.join(curr_dir, f"{graph_str}.mmd"), "w", encoding="utf-8") as f:
            f.write(graph_mermaid)


    def _print_stream(self,stream):
        for s in stream:
            messages = s["messages"][-1]
            print(f"Stream item type: {type(s)}")
            print(f"Stream item content: {s}")
            if "tool_calls" in s:
                print(f"Tool calls: {s['tool_calls']}")
            if "tool_results" in s:
                print(f"Tool results: {s['tool_results']}")
            
            if isinstance(messages, tuple):
                print(f"Tuple message: {messages}")
            else:
                try:
                    print(f"Message content: {messages.content}")
                    messages.pretty_print()
                except AttributeError:
                    print(f"Cannot pretty print: {messages}")



    #######################################################################################
    ###                                    GENERATE                                     ###
    #######################################################################################
    def parse_node(self, state:BasicState):

        requirements_list, out_rule_string = list(), list()
        langda_pattern = r'langda\("([^"\\]*(\\.[^"\\]*)*?)"\)'
        
        for line in rule_string.split('\n'):
            if 'langda' in line:
                modified_line = re.sub(
                    langda_pattern, 
                    lambda m: (requirements_list.append(f"\nRequirement:\n{m.group(1)}\n")) or "\n{{LANGDA}}\n", 
                    line
                )
                out_rule_string.append(modified_line)
            else:
                out_rule_string.append(line)

        return {"prompt_rule_template":'\n'.join(out_rule_string),
                "prompt_rule_requirements":requirements_list}


    def generate_node(self,state:BasicState):
        state["status"] = TaskStatus.CODE_GENERATION

        prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful assistant that helps the user to generate deepproblog code."),
                    ("human", self.prompt_template)
                ])
        input={
            "context": state["user_context"],
            "requirements": state["prompt_rule_requirements"],
            "result": "result(win=X, T)",
            "rule_set":state["prompt_rule_template"],
        }
        
        chain = prompt | self.model | StrOutputParser()
        result = chain.invoke(input=input, config=self.config)
        # Abstract code blocks.
        generated_codes = []
        pattern = r"```(?:prolog|[a-z]*)?\n(.*?)```"
        matches = re.findall(pattern, result, re.DOTALL)
        for match in matches:
            generated_codes.append(match)
        return {
            "generated_codes":generated_codes
        }
    
    def reconstruct_rule_node(self,state:BasicState):
        pattern = r"\{\{LANGDA\}\}"
        repl_iter = iter(state["generated_codes"])
        new_rule_string = re.sub(pattern, lambda _: next(repl_iter), state["prompt_rule_template"])
        with open(os.path.join(cf.CURRENT_PATH, self.path_to_rule), "w") as f:
            f.write(new_rule_string)

        return {
            "generated_new_ruleset":new_rule_string
        }
    
    def call_gen_workflow(self):

        gen_workflow = StateGraph(BasicState)
        gen_workflow.set_entry_point("parse_node")
        gen_workflow.add_node("parse_node", self.parse_node)
        gen_workflow.add_node("generate_code", self.generate_node)
        gen_workflow.add_node("reconstruct_rule",  self.reconstruct_rule_node)
        
        gen_workflow.add_edge("parse_node", "generate_code")
        gen_workflow.add_edge("generate_code", "reconstruct_rule")
        gen_workflow.set_finish_point("reconstruct_rule")

        gen_subgraph = gen_workflow.compile()
        self.state = gen_subgraph.invoke(self.state, config=self.config)
        print("===============generated_new_ruleset:===============\n")
        print(self.state["generated_new_ruleset"])

        self._draw_mermaid_png(gen_subgraph, "gen_subgraph")



    #######################################################################################
    ###                                      TEST                                       ###
    #######################################################################################
    def test_node(self, state:BasicState):
        print("test_node",state)
        state["status"] = TaskStatus.CODE_TESTING
        agent = create_react_agent(
            model = self.model, 
            tools = self.tools,
        )

        query = (
            f"please test, use biased test data. With the rule set {self.path_to_rule}"
        )
        result = self._print_stream(agent.stream(input={"messages": [("user",query)]}, 
                                config=self.config,
                                stream_mode="values"))
        return {"test_results":result}

    def feedback_node(self, state: BasicState):
        while True:
            user_feedback = input("Are you satisfied with the results? (yes/no): ").strip().lower()

            if user_feedback in ("yes", "y"):
                print("Great! Task marked as completed.")
                return {"status":TaskStatus.COMPLETED}

            elif user_feedback in ("no", "n"):
                user_advice = input("Could you tell me the specific reason? ").strip()
                state["user_feedback"] = user_advice
                print("Thanks for your feedback! Task marked as failed.")
                return {"status":TaskStatus.FAILED}

            else:
                print("Invalid input. Please answer 'yes' or 'no'.")


    def _decide_next(self,state:BasicState):
        if state["status"] == TaskStatus.COMPLETED:
            return END
        elif state["status"] == TaskStatus.FAILED:
            return "test_node"
        
    
    def call_test_workflow(self):
        
        test_workflow = StateGraph(BasicState)
        test_workflow.set_entry_point("test_node")
        test_workflow.add_node("test_node", self.test_node)
        test_workflow.add_node("feedback_node", self.feedback_node)

        test_workflow.add_conditional_edges("feedback_node",self._decide_next)
        test_workflow.add_edge(start_key="test_node", end_key='feedback_node')

        test_subgraph = test_workflow.compile(checkpointer=self.checkpointer)
        self.state = test_subgraph.invoke(self.state,config=self.config)

        self._draw_mermaid_png(test_subgraph, "test_subgraph")




if __name__ == "__main__":
    rule_string = ""
    with open ("examples/LANGDA/drone_with_langchain/rules/basic/drone.pl") as f:
        rule_string += f.read()
    l = Langda_Agent(rule_string)
    print(l.call_gen_workflow())
    print(l.call_test_workflow())

