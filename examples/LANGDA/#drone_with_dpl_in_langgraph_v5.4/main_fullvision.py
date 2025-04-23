import re
import os
import json
import time
from typing import List, Dict

from langchain import hub
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import create_react_agent, ToolNode
from langchain_core.output_parsers.string import StrOutputParser

from state import BasicState, TaskStatus, Mode, LangdaItem, FullLangdaDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain.tools import BaseTool

from config import paths
from parser import integrated_code_parser
from tools_v1 import CustomTestTool, CustomSearchTool, CustomTrainTool
"""
Full vision means that LLM processes the complete prompt uniformly and generates all code content at the same time.

"""
class Langda_Agent(object):
    def __init__(self, rule_string:str, addition_input:dict={"prefix":"","user_context":"","error_report":""}, caching:bool=False, saving:bool=False):
        # self.rule_string, self.requirements_list = self._parse(rule_string)
        self.prefix:str = addition_input["prefix"]
        self.generated_codes = list()
        self.generate_prompt:str = paths.load_prompt("generate")
        self.evaluate_prompt:str = paths.load_prompt("evaluate")
        self.regenerate_prompt:str = paths.load_prompt("regenerate")

        self.langda_placeholder = "{{LANGDA}}"# r"\{\{LANGDA\}\}"
        self.state = BasicState()
        self.state["user_context"] = addition_input["user_context"]
        self.state["error_report"] = addition_input["error_report"]
        self.state["rule_string"] = rule_string
        self.config = {"configurable": {"thread_id": "2"}}
        self.checkpointer = MemorySaver()

        self.model=ChatDeepSeek(
            model="deepseek-chat", 
            temperature=0,
            api_key="sk-293f9d735260457583c3cbe0df475d4f")
        self.tools = [
                CustomTestTool(),
            ]

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

    def _replace_placeholder(self,template:str, replacement_list:list, placeholder="{{LANGDA}}") -> str:
        segments = template.split(placeholder)
        # segments[0] + (N times [replacement or placeholder] + segments[1..])
        result = segments[0]
        # 遍历每个段后面应该插入的内容
        for i, seg in enumerate(segments[1:]):
            if i < len(replacement_list) and replacement_list[i] is not None:
                result += replacement_list[i]
            else:
                result += placeholder
            result += seg
        return result
    
    def _select_mode(self, state:BasicState, langda_dict):
        keys = set(langda_dict.keys())
        if not "NET" in keys and not "LLM" in keys:
            if len(keys) >= 1:
                state["mode"] = Mode.PURE_PAR
            else:
                raise KeyError("forget to set langda parameter?")

        elif not "NET" in keys and "LLM" in keys:
            if len(keys) > 1:
                state["mode"] = Mode.PARA_LLM
            else:
                state["mode"] = Mode.PURE_LLM

        elif "NET" in keys and not "LLM" in keys:
            if len(keys) > 1:
                state["mode"] = Mode.FULL_LLM  
            else:
                state["mode"] = Mode.PURE_NET

        else:
            if len(keys) > 2:
                state["mode"] = Mode.FULL_LLM  
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
        print("processing parse_node...")
        # replace all langda predicate to forms like: langda(X,Y,...)
        # parser = LangdaParser()
        # prompt_template, lann_dicts, langda_dicts = parser.parse(state["rule_string"])
        prompt_template, lann_dicts, langda_dicts = integrated_code_parser(state["rule_string"])
        # construct part one of the deepproblog block

        paths.save_as_file(prompt_template,"prompt_template","1st")

        # print("full_dict_list:",full_dict_list)

        return {"prompt_template":"\n".join(prompt_template),     # the string that only leave "{LANGDA}" slot for prompting
                "lann_dicts":lann_dicts,                        # the dict that contains detail informations about network
                "langda_dicts":langda_dicts}                     # the dict that contains detail informations about langda


    def requirements_node(self,state:BasicState):
        """
        ugly! please fix later...
        """
        print("processing requirements_node...")

        lann_dicts:List[Dict[str,str]] = state["lann_dicts"]
        langda_dicts:List[Dict[str,str]] = state["langda_dicts"]
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
                    raise ValueError(f"langda has UNEXPECTED term:{key}")
            if not head:
                requirements.append(f"The Information for Generating Code of {self._ordinal(n)} Placeholder: ")
            else:
                requirements.append(f"The Information for Generating Code of {self._ordinal(n)} Placeholder, ")
                requirements.append(f"inside the Parent Predicate: {head}")
            if tools: # List of Tools
                requirements.append(f"The Tools that you could use: {tools}")
            if llm: # LLM prompt
                requirements.append(f"Requirements of Rules: {llm}")
            if net: # Decription of networks
                requirements.append(f"Network Requirements: {net}")

            requirements.append("\n")

        requirements_str = "\n".join(requirements)
        with open(os.path.join(paths.base_dir,"history/requirements.txt"),"w") as f:
            f.write(requirements_str)
        return{"prompt_requirements":requirements_str,}

    def generate_node(self,state:BasicState):
        print("processing generate_node...")
        new_iter_count = state["iter_count"] + 1

        state["status"] = TaskStatus.GNRT
        # print("\n===============langda_dicts:===============\n",state["langda_dicts"])
        prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful assistant that helps the user to generate deepproblog code."),
                    ("human", self.generate_prompt)
                ])
        input={
            "context": state["user_context"],
            "requirements": state["prompt_requirements"],
            "rule_set":state["prompt_template"],
        }
        chain = prompt | self.model | StrOutputParser()
        result = chain.invoke(input=input, config=self.config)
        # Abstract code blocks.

        paths.save_as_file(result,"generated_result")

        generated_codes = []
        pattern = r"```(?:prolog|[a-z]*)?\n(.*?)```"
        matches = re.findall(pattern, result, re.DOTALL)
        if matches:
            for match in matches:
                generated_codes.append("% === % LLM Generated Logic Codes % === %\n"+match+"% === % ========================= % === %")

            return {
                "iter_count": new_iter_count,
                "generated_codes":generated_codes
            }
        else:
            raise ValueError("generate_node: Generated code no found...")

    def reconstruct_rule_node(self,state:BasicState):
        print("processing reconstruct_rule_node...")
        new_iter_count = state["iter_count"] + 1

        final_code = self._replace_placeholder(state["prompt_template"],state["generated_codes"], self.langda_placeholder)

        paths.save_as_file(final_code,"final_code",self.prefix)

        return {
            "final_code":final_code,
            "iter_count":new_iter_count
        }
    
    def construct_gen_workflow(self):

        gen_workflow = StateGraph(BasicState)
        gen_workflow.set_entry_point("parse_node")
        gen_workflow.add_node("parse_node", self.parse_node)
        gen_workflow.add_node("requirements_node", self.requirements_node)
        gen_workflow.add_node("generate_code", self.generate_node)
        gen_workflow.add_node("reconstruct_rule",  self.reconstruct_rule_node)

        gen_workflow.add_edge("parse_node", "requirements_node")
        gen_workflow.add_edge("requirements_node", "generate_code")
        gen_workflow.add_edge("generate_code", "reconstruct_rule")
        gen_workflow.set_finish_point("reconstruct_rule")

        # self.state = gen_subgraph.invoke(self.state, config=self.config)
        # print("===============final_code:===============\n")
        # print(self.state["final_code"])
        # self._draw_mermaid_png(gen_subgraph, "gen_subgraph")
        return gen_workflow



    #######################################################################################
    ###                                      TEST                                       ###
    #######################################################################################
    def test_node(self, state:BasicState):
        print("processing test_node...")

        state["status"] = TaskStatus.TEST
        constructed_code_list = []
        pattern = r"```report\s+(.*?)```"

        for i, code in enumerate(state["generated_codes"]):
            constructed_code_list.append(f"The {self._ordinal(i)} Code Block That You Should Analyse:")
            constructed_code_list.append(code)
            constructed_code_list.append("\n")

        prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful assistant that helps the user to generate deepproblog code."),
                    ("human", self.evaluate_prompt)
                ])
        input={
            "error_report": state["error_report"],
            "context": state["user_context"],
            "output": state["final_code"],
            "code_list":"\n".join(constructed_code_list),
        }
        chain = prompt | self.model | StrOutputParser()
        evaluated_result = chain.invoke(input=input, config=self.config)

        paths.save_as_file(evaluated_result, "evaluated_result")

        raw_evaluated_codes = re.findall(pattern, evaluated_result, re.DOTALL)
        evaluated_codes:List[dict] = []
        for raw in raw_evaluated_codes:
            try:
                evaluated_codes.append(json.loads(raw))
            except ValueError:
                evaluated_codes.append(None)

        return {
            "evaluated_result":evaluated_result,
            "evaluated_codes":evaluated_codes,
            }

    def _decide_next(self, state:BasicState):
        print("processing _decide_next...")
        print("#current round:",state["iter_count"])
        to_end = True
        for report in state["evaluated_codes"]:
            print(report["Need_regenerate"])
            if report["Need_regenerate"] == "True":
                to_end = False
        if to_end or state["iter_count"] >= 3:
            state["status"] = TaskStatus.CMPL
            return "summary_node"
        else:
            return "regenerate_node"

    def regenerate_node(self, state:BasicState):
        """
        Regenerate specific code blocks based on evaluation.
        """
        print("processing regenerate_node...")
        state["status"] = TaskStatus.GNRT
        # Create a prompt to regenerate specific blocks
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that helps the user to fix errors in deepproblog code."),
            ("human", self.regenerate_prompt)
        ])
        fest_code_list = [] # the codes that does not to regenerate
        code_with_report_list = []
        regenerate_indices = []
        for i, (code, report) in enumerate(zip(state["generated_codes"],state["evaluated_codes"])):
            if report["Need_regenerate"] == "True":
                fest_code_list.append(None)
                regenerate_indices.append(i)

                code_with_report_list.append(f"### The {self._ordinal(i)} Code Block:")
                code_with_report_list.append(code)
                code_with_report_list.append(f"It's corresponding analysis:")
                code_with_report_list.append(report["Report"])
                code_with_report_list.append("\n")
            else:
                fest_code_list.append(code)

        # Prepare input for the regeneration prompt
        regenerate_template = self._replace_placeholder(state["prompt_template"],fest_code_list, self.langda_placeholder)
        print("=====================regenerate_template=====================\n",regenerate_template)
        print("=============================================================\n")
        input={
            "context": state["user_context"],
            "rule_set": regenerate_template,
            "blocks_with_analysis":"\n".join(code_with_report_list),
        }
        # Run the regeneration
        chain = prompt | self.model | StrOutputParser()
        result = chain.invoke(input=input, config=self.config)

        # Extract the regenerated code blocks
        pattern = r"```(?:prolog|[a-z]*)?\n(.*?)```"
        regenerated_codes = re.findall(pattern, result, re.DOTALL)
        if len(regenerated_codes) != len(regenerate_indices):
            raise ValueError("The amount of code generated does not matches the number of code blocks that need to be regenerated")
        
        paths.save_as_file(regenerated_codes,"generated_codes","re")
        paths.save_as_file(code_with_report_list,"evaluated_codes","&code")

        return {
            "generated_codes":regenerated_codes,
            "prompt_template":regenerate_template, 
        }

    def summary_node(self, state:BasicState):
        print("processing summary_node...")
        state["endtime"] = time.time()
        running_time = round(state["endtime"]-state["srttime"])
        print("running_time",running_time)
        print("total round:",state["iter_count"])
        # some other summaries...

        return state

    def call_main_workflow(self):
        self.state["srttime"] = time.time()
        self.state["iter_count"] = 0

        test_workflow = StateGraph(BasicState)
        test_workflow.set_entry_point("generate_workflow")
        test_workflow.add_node("generate_workflow", self.construct_gen_workflow().compile())
        test_workflow.add_node("test_node", self.test_node)
        test_workflow.add_node("regenerate_node", self.regenerate_node)
        test_workflow.add_node("summary_node", self.summary_node)

        test_workflow.add_edge(start_key="generate_workflow", end_key='test_node')
        test_workflow.add_conditional_edges("test_node",self._decide_next, 
            {
                "regenerate_node": "regenerate_node",
                "summary_node": "summary_node"
            })
        test_workflow.add_edge(start_key="regenerate_node", end_key='test_node')
        test_workflow.set_finish_point("summary_node")

        # test_workflow.add_edge(start_key="test_node", end_key='feedback_node')

        test_subgraph = test_workflow.compile(checkpointer=self.checkpointer)
        self.state = test_subgraph.invoke(self.state, config=self.config)

        self._draw_mermaid_png(test_subgraph, "main_subgraph")

if __name__ == "__main__":
    addition = {}
    addition["user_context"] = """
    please notice distance(X, Y) is a value, so please do not create single clause like: distance(X, bomb) > 10.
    please seen initial_charge, charge_cost and weight as value and use in following form:
    V is value, value < 5 or value > 10...
    """
    rules_string = ""
    rule_path = "/Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/examples/LANGDA/#drone_with_dpl_in_langgraph_v5.4/rules/"
    # /Users/zhenzhili/MASTERTHESIS/\#Expert_System_Design/examples/LANGDA/\#drone_with_dpl_in_langgraph_v5.4/process_fullvision.py /rules/addition_prompt.pl
    # with open (os.path.join(rule_path,"test/addition_prompt.pl"),"r") as f:
    with open (os.path.join(rule_path,"test/promis_prompt.pl"),"r") as f:
        rules_string += f.read()

    l = Langda_Agent(rules_string)
    l.call_main_workflow()

