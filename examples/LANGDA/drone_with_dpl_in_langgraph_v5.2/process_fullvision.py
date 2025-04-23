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
import parse as pr
from tools_v1 import CustomTestTool, CustomSearchTool, CustomTrainTool
"""
Full vision means that LLM processes the complete prompt uniformly and generates all code content at the same time.

"""
class Langda_Agent(object):
    def __init__(self, rule_string:str, addition_input:dict={"user_context":"..."}, caching:bool=False, saving:bool=False):
        # self.rule_string, self.requirements_list = self._parse(rule_string)
        self.generated_codes = list()
        self.prompt_template:str = cf.SYSTEM_PROMPT_FORMAT_LANGDA_FULLVISION
        self.langda_placeholder = "[[LANGDA]]"# r"\{\{LANGDA\}\}"
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
        replace_net = "{NET}"
        replace_llm = self.langda_placeholder
        slot_text = f"% {replace_net}% {replace_llm}" # it will be inserted in front of the code block, and used for prompting

        result_dict_list, result_text = pr.langda_parser(state["rule_string"]) # result_dict_list: X, Langda, NET, LLM
        lines_with_slot, lines_contain_langda = pr.find_predicates_and_add_slot_in_line(result_text,slot_text) # lines, list(head, start_line, end_line)
        result_lines = lines_with_slot
        result_string = '\n'.join(result_lines)
        full_dict_list:FullLangdaDict = []

        DEEPPROBLOG_PART_ONE = []
        # for line in result_lines:
        net = 0
        for i,(head, code_block, count) in enumerate(lines_contain_langda):             # form: coin_win() :- langda(X,T), permits(X), langda(X,Y,Z).
            unpack_networks_string:List[str] = []
            current_predicate_list:List[LangdaItem] = []

            # deal with network, and construct new problog for prompt in a list called "lines"
            while count > 0: # form: langda(X,Y), (16,18)
                # self._select_mode(state,langda_dict) # set mode for state
                if "NET" in result_dict_list[net].keys():
                    unpack_networks_string.append(result_dict_list[net]["NET"])
                current_predicate_list.append({
                    **result_dict_list[net]
                })
                net += 1
                count -= 1

            unpack_networks_list = pr.parse_all_networks(unpack_networks_string)
            DEEPPROBLOG_PART_ONE.append(unpack_networks_list)
            full_dict_list.append({"Block":code_block,
                                   "Head":head,
                                   "Langda": current_predicate_list
                                   })

        # construct part one of the deepproblog block
        out_rule_string = self._replace_placeholder(result_string, DEEPPROBLOG_PART_ONE, replace_net)
        with open(os.path.join(cf.CURRENT_PATH,"history/out_rule_string.pl"), "w") as f:
            f.write(out_rule_string)
        with open(os.path.join(cf.CURRENT_PATH,"history/full_dict_list.txt"), "w") as f:
            json.dump(full_dict_list,f, indent=4)
        # print("full_dict_list:",full_dict_list)
        print("out_rule_string:",out_rule_string)
        return {"prompt_rule_template":out_rule_string,     # the string that only leave "{LLM}" slot for prompting
                "prompt_rule_dict":full_dict_list}  # the dict that contains detail informations

    def decision_node(self,state:BasicState):
        """
        ugly! please fix later...
        """
        prompt_rule_dict:FullLangdaDict = state["prompt_rule_dict"]
        out_rule_string:str = state["prompt_rule_template"]
        requirements = []
        for rule_dict in prompt_rule_dict:
            llm_value = self.langda_placeholder
            if "LLM" not in rule_dict["Langda"]:
                llm_value = ""
            out_rule_string = out_rule_string.replace(self.langda_placeholder, llm_value)
        
        # Construct the requirement part of prompt:
        for rule_dict in prompt_rule_dict:
            if rule_dict["Head"] == "none":
                requirements.append(f"The Requirement for Standalone/Leaf Langda Predicate:")
            else:
                requirements.append(f"The Requirement for Parent Predicate of Langda: {rule_dict['Head']}")

            for langda_item in rule_dict["Langda"]:
                for key,value in langda_item.items():
                    if key == "LLM":
                        requirements.append(f"The Requirement of {langda_item['Langda']}: {langda_item['LLM']}")
                    elif key == "NET":
                        requirements.append(f"It has corrsponding event predicate")
                    else:
                        requirements.append(f"The Meaning of Term {key}: {value}")
                        continue
                requirements.append("\n")
        requirements_str = "\n".join(requirements)
        with open(os.path.join(cf.CURRENT_PATH,"history/requirements.txt"),"w") as f:
            f.write(requirements_str)
        return{"prompt_requirements":requirements_str,}

    def generate_node(self,state:BasicState):
        state["status"] = TaskStatus.CODE_GENERATION
        print("\n===============prompt_rule_template:===============\n",state["prompt_rule_template"])
        # print("\n===============prompt_rule_dict:===============\n",state["prompt_rule_dict"])
        prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful assistant that helps the user to generate deepproblog code."),
                    ("human", self.prompt_template)
                ])
        input={
            "context": state["user_context"],
            "requirements": state["prompt_rule_dict"],
            "result": state["prompt_requirements"],
            "rule_set":state["prompt_rule_template"],
        }
        
        chain = prompt | self.model | StrOutputParser()
        result = chain.invoke(input=input, config=self.config)
        # Abstract code blocks.
        with open (os.path.join(cf.CURRENT_PATH,"history/result_from_llm.txt"),"w") as f:
            f.write(result)
        generated_codes = []
        pattern = r"```(?:prolog|[a-z]*)?\n(.*?)```"
        matches = re.findall(pattern, result, re.DOTALL)
        for match in matches:
            generated_codes.append("% ---------------------------- LLM Generated Logic Codes ------------------------------- %\n"+match)

        return {
            "generated_new_codes":generated_codes
        }
    
    def reconstruct_rule_node(self,state:BasicState):
        new_rule_string = self._replace_placeholder(state["prompt_rule_template"],state["generated_new_codes"], self.langda_placeholder)
        # repl_iter = iter(state["generated_new_codes"])
        # new_rule_string = re.sub(self.langda_placeholder, lambda _: next(repl_iter), state["prompt_rule_template"])
        with open(os.path.join(cf.CURRENT_PATH, self.path_to_rule), "w") as f:
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
        with open(os.path.join(cf.CURRENT_PATH,"history/generated_new_ruleset.txt"), "w") as f:
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
    # rule_string = ""
    # with open ("/Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/examples/MNIST/#drone_with_dpl_in_langgraph_v5.2/rules/landa_example_predicate.pl") as f:
    #     rule_string += f.read()

            
    l = Langda_Agent(pr.full_text_for_parse_test)
    # l.parse_node({"rule_string":pr.full_text_for_parse_test})
    print(l.call_gen_workflow())
    # print(l.call_test_workflow())

