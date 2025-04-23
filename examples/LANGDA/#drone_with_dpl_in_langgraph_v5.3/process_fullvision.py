import re
import os
import json
from typing import List, Dict
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

from state import BasicState, TaskStatus, Mode, LangdaItem, FullLangdaDict
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_deepseek import ChatDeepSeek
from langchain.tools import BaseTool

import config as cf
from parser import LangdaParser, full_text_for_parse_test
from _beautiful_addition import integrated_code_parser
from tools_v1 import CustomTestTool, CustomSearchTool, CustomTrainTool
"""
Full vision means that LLM processes the complete prompt uniformly and generates all code content at the same time.

"""
class Langda_Agent(object):
    def __init__(self, rule_string:str, addition_input:dict={"user_context":"..."}, caching:bool=False, saving:bool=False):
        # self.rule_string, self.requirements_list = self._parse(rule_string)
        self.generated_codes = list()
        self.prompt_template:str = cf.SYSTEM_PROMPT_FORMAT_LANGDA_FULLVISION
        self.langda_placeholder = "{{LANGDA}}"# r"\{\{LANGDA\}\}"
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


    # def _construct_prompt(self) -> ChatPromptTemplate:

    #     return ChatPromptTemplate.from_messages([
    #         ("system", "You are a helpful assistant that helps the user to generate deepproblog code."),
    #         ("human", self.prompt_template)
    #     ])
    def _ordinal(self, n:int) -> str:
        # from int number generate ordinal: 1st,2nd,3rd,4th,5th,...
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return str(n) + suffix
    def _draw_mermaid_png(self,graph:StateGraph, graph_str:str):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        graph_mermaid = graph.get_graph().draw_mermaid()
        with open(os.path.join(curr_dir, f"history/{graph_str}.mmd"), "w", encoding="utf-8") as f:
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

    def _replace_placeholder(self,template:str, replacement_list:list, placeholder="{{NET}}") -> str:
        result = template
        for item in replacement_list:
            if placeholder in result:
                result = result.replace(placeholder, str(item), 1)
        return result
    
    def _select_mode(self, state:BasicState, langda_dict):
        keys = set(langda_dict.keys())
        if not "NET" in keys and not "LLM" in keys:
            if len(keys) >= 1:
                state["mode"] = Mode.PURE_PARAM
            else:
                raise KeyError("forget to set langda parameter?")

        elif not "NET" in keys and "LLM" in keys:
            if len(keys) > 1:
                state["mode"] = Mode.LLM_WITH_RETURN
            else:
                state["mode"] = Mode.PURE_LLM

        elif "NET" in keys and not "LLM" in keys:
            if len(keys) > 1:
                state["mode"] = Mode.FULL_PART  
            else:
                state["mode"] = Mode.PURE_NET

        else:
            if len(keys) > 2:
                state["mode"] = Mode.FULL_PART  
            else:
                state["mode"] = Mode.ELSE


    #######################################################################################
    ###                                    GENERATE                                     ###
    #######################################################################################
    def parse_node(self, state:BasicState):
        """
        there are two special terms that defined in langda predicate:
        NET:"[mnist_net1(0,1), mnist_net2(2,3)]"
        LLM:"some natural language descriptions..."
        they won't show up in final langda predicate, and only used to construct the deepproblog code.
        """
        # replace all langda predicate to forms like: langda(X,Y,...)
        # parser = LangdaParser()
        # out_rule_list, lann_dicts, langda_dicts = parser.parse(state["rule_string"])
        out_rule_list, lann_dicts, langda_dicts = integrated_code_parser(state["rule_string"])
        # construct part one of the deepproblog block
        with open(os.path.join(cf.CURRENT_PATH,"history/parse_code.txt"), "w") as f:
            f.write("\n".join(out_rule_list))
        with open(os.path.join(cf.CURRENT_PATH,"history/langda_dicts.txt"), "w") as f:
            json.dump(lann_dicts,f, indent=4)
        with open(os.path.join(cf.CURRENT_PATH,"history/langda_dicts.txt"), "a") as f:
            json.dump(langda_dicts,f, indent=4)
        # print("full_dict_list:",full_dict_list)

        return {"prompt_rule_template":"\n".join(out_rule_list),     # the string that only leave "{LLM}" slot for prompting
                "prompt_net_dict":lann_dicts,                        # the dict that contains detail informations about network
                "prompt_rule_dict":langda_dicts}                     # the dict that contains detail informations about langda


    def decision_node(self,state:BasicState):
        """
        ugly! please fix later...
        """
        lann_dicts:List[Dict[str,str]] = state["prompt_net_dict"]
        langda_dicts:List[Dict[str,str]] = state["prompt_rule_dict"]
        requirements = []            
        # Construct the requirement part of prompt:
        if lann_dicts:
            requirements.append(f"The Information of Networks:")
            for net_dict in lann_dicts:
                requirements.append(f"The Information of Network: {net_dict['nn']:}")
                for key, value in net_dict.items():
                    if not key == 'nn':
                        requirements.append(f"For the term: {key}, user says: {value}")
            requirements.append("\n")

        for n,langda_dict in enumerate(langda_dicts):
            head, tools, llm, net = "", "", "", ""
            for key,value in langda_dict.items():
                if key == "HEAD": # List of Tools
                    head = value.strip()
                elif key == "LOT": # List of Tools
                    tools = value.strip()
                elif key == "LLM": # List of Tools
                    llm = value.strip()
                elif key == "NET": # List of Tools
                    net = value.strip()
                else:
                    raise ValueError("langda has UNEXPECTED term.")
                
                if key == "HEAD": # List of Tools
                    if head:
                        requirements.append(f"The Information for Generating Code of {self._ordinal(n)} Placeholder: ")
                    else:
                        requirements.append(f"The Information for Generating Code of {self._ordinal(n)} Placeholder, ")
                        requirements.append(f"inside the Parent Predicate: {langda_dict['HEAD']}")
                if tools: # List of Tools
                    requirements.append(f"The Tools that you could use: {langda_dict['LOT']}")
                if llm: # LLM prompt
                    requirements.append(f"Requirements of Rules: {langda_dict['LLM']}")
                if net: # Decription of networks
                    requirements.append(f"Network Requirements: {langda_dict['NET']}")

            requirements.append("\n")

        requirements_str = "\n".join(requirements)
        with open(os.path.join(cf.CURRENT_PATH,"history/requirements.txt"),"w") as f:
            f.write(requirements_str)
        return{"prompt_requirements":requirements_str,}

    def generate_node(self,state:BasicState):
        state["status"] = TaskStatus.CODE_GENERATION
        # print("\n===============prompt_rule_dict:===============\n",state["prompt_rule_dict"])
        prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful assistant that helps the user to generate deepproblog code."),
                    ("human", self.prompt_template)
                ])
        input={
            "context": state["user_context"],
            "requirements": state["prompt_requirements"],
            "rule_set":state["prompt_rule_template"],
        }
        chain = prompt | self.model | StrOutputParser()
        result = chain.invoke(input=input, config=self.config)
        # Abstract code blocks.

        with open (os.path.join(cf.CURRENT_PATH, "history/result_from_llm.txt"), "w") as f:
            f.write(result)
        
        generated_codes = []
        pattern = r"```(?:prolog|[a-z]*)?\n(.*?)```"
        matches = re.findall(pattern, result, re.DOTALL)
        if matches:
            for match in matches:
                generated_codes.append("% === % LLM Generated Logic Codes % === %\n"+match+"\n% === % ========================= % === %\n")

            return {
                "generated_new_codes":generated_codes
            }
        else:
            raise ValueError("generate_node: Generated code no found...")

    def reconstruct_rule_node(self,state:BasicState):
        new_rule_string = self._replace_placeholder(state["prompt_rule_template"],state["generated_new_codes"], self.langda_placeholder)
        # repl_iter = iter(state["generated_new_codes"])
        # new_rule_string = re.sub(self.langda_placeholder, lambda _: next(repl_iter), state["prompt_rule_template"])
        with open(cf.GENERATED_RULE_PATH, "w") as f:
            f.write(new_rule_string)

        return {
            "generated_new_ruleset":new_rule_string
        }
    
    def call_gen_workflow(self):

        gen_workflow = StateGraph(BasicState)
        gen_workflow.set_entry_point("parse_node")
        gen_workflow.add_node("parse_node", self.parse_node)
        gen_workflow.add_node("decision_node", self.decision_node)
        gen_workflow.add_node("generate_code", self.generate_node)
        gen_workflow.add_node("reconstruct_rule",  self.reconstruct_rule_node)
        
        gen_workflow.add_edge("parse_node", "decision_node")
        gen_workflow.add_edge("decision_node", "generate_code")
        gen_workflow.add_edge("generate_code", "reconstruct_rule")
        gen_workflow.set_finish_point("reconstruct_rule")

        gen_subgraph = gen_workflow.compile()
        self.state = gen_subgraph.invoke(self.state, config=self.config)
        print("===============generated_new_ruleset:===============\n")
        print(self.state["generated_new_ruleset"])
        with open(os.path.join(cf.CURRENT_PATH,"history/generated_new_ruleset.pl"), "w") as f:
            f.write(self.state["generated_new_ruleset"])
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
    with open ("/Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/examples/LANGDA/#drone_with_dpl_in_langgraph_v5.3/rules/langda_ruleset/ProMis_with_langda.pl","r") as f:
        rule_string += f.read()

    l = Langda_Agent(rule_string)
    # l.parse_node({"rule_string":pr.full_text_for_parse_test})
    print(l.call_gen_workflow())
    # print(l.call_test_workflow())

