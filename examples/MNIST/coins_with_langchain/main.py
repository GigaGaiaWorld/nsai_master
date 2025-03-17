
import os
import re

from typing import Union, List, Callable, Dict, Any
from langchain_core.agents import AgentAction, AgentFinish
from langchain.schema.runnable import Runnable
from langchain_core.outputs.llm_result import LLMResult

from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.output_parsers.list import MarkdownListOutputParser
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser

from langchain_core.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain_deepseek import ChatDeepSeek
from langchain.agents import tool, Tool
from langchain.agents.format_scratchpad.log import format_log_to_str
from langchain.tools.render import render_text_description


from dotenv import load_dotenv

current_path = os.path.dirname(os.path.abspath(__file__))
rules_dir = os.path.join(current_path, "rules")
data_dir = os.path.join(current_path, "data")
src_dir = os.path.normpath(os.path.join(current_path, "../../../src"))
myprompt_dir = os.path.join(src_dir, "prompts/My_prompt")
load_dotenv(os.path.join(src_dir, ".env"))

class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(
            self, serialized:Dict[str, Any], prompts:List[str], **kwargs:Any
        ) -> Any:
        """Run when LLM start running."""
        print(f"***Prompt to LLM was:***\n{prompts[0]}")
        print("=====================================")

    def on_llm_end(
            self, response: LLMResult, **kwargs:Any
        ) -> Any:
        """Run when LLM end running."""
        print(f"***LLM Response was:***\n{response.generations[0][0].text}")
        print("=====================================")

def read_file(data_path, file_name, read_samples=False) -> str:
    """
    read file from path, and return as string
    """
    file_path = os.path.join(data_path, file_name)
    with open(file_path) as f:
        if not read_samples:
            file_str = f.read()
        else:
            file_lines = f.readlines()[:5]
            file_str = "\n".join(file_lines)
    return file_str

def extract_prolog_code(text):
    """Extract code blocks of specified language from text"""
    pattern = f"```prolog\\s*(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return matches
    return []

if __name__ == "__main__":
    print("langchain launching...")

    ### ==================== template (without any dynamic variable) ================= ###
    template:str = read_file(myprompt_dir, "translation_inline.txt")

    ### ============================== dynamic variable ============================== ###
    context_str:str ="""
    This code combines the outputs of two different neural networks (corresponding to event1 and event2 respectively), 
    extracts information from the simultaneous events through logical rules, and determines the final event outcome based on the difference between the two event labels.
    """
    # queries_str = read_file(data_path, "result_test_data.txt",read_samples=True)
    queries_str:str = "result(win=A,T)"
    # question_str_basic = """
    # # When the absolute value of the difference between the outputs of e1 and e2 is 2, the win output is 1, otherwise the game output is 0
    # """
    question_str_basic:str = ""
    # question_str_additional = ""
    question_str_additional:str = """
    Additional Rules:
    when the timestamp is between 50 and 250, if the event1 and event2 are classified as 1 and 3, the win output is 0
    when the timestamp is between 100 and 300, if the event1 and event2 are classified as 0 and 3, the win output is 1
    """
    rules_str:str = read_file(rules_dir, "basic/DeE_ResDeE.pl")
    facts_str:str = read_file(data_dir, "origin/in_test_data.txt",read_samples=True)

    ### ============================= tools(empty for now) =========================== ###
    tools:List[Tool]

    ### =============================== define the agent ============================= ###
    prompt_template:PromptTemplate = PromptTemplate.from_template(template=template)
    prompt:str = prompt_template.partial(
            context=context_str,
            queries=queries_str,
        )

    llm:ChatDeepSeek = ChatDeepSeek(
            temperature=0.3, 
            model="deepseek-chat",
            stop_sequences=["\nObservation"],
            callbacks=[AgentCallbackHandler()]
        )

    agent:Runnable = (
        {
            "rule_set":lambda x: x["rule_set"], 
            "facts":lambda x: x["facts"], 
            "question":lambda x: x["question"], 
        }
        | prompt 
        | llm 
        # | MarkdownListOutputParser()
        | StrOutputParser()
        | extract_prolog_code
    )

    ### =============================== invoke the agent ============================= ###
    agent_step = agent.invoke(
            input={
                "rule_set":rules_str, 
                "facts":facts_str, 
                "question":question_str_basic+"\n"+question_str_additional, 
            }
    )
    # agent_step = ""
    # while not isinstance(agent_step, AgentFinish):
    #     # (method) def invoke(input: Any, config: RunnableConfig | None = None, **kwargs: Any) -> (AgentAction | AgentFinish)
    #     agent_step: Union[AgentAction,AgentFinish] = agent.invoke(
    #         {
    #         "rule_set":rules_str, 
    #         "facts":facts_str, 
    #         "question":question_str_basic+"\n"+question_str_additional, 
    #         }
    #     )

    #     # print(agent_step)
    #     if isinstance(agent_step, AgentAction):
    #         tool_name:str = agent_step.tool
    #         tool_to_use:Tool = find_tool_by_name(tools, tool_name)

    #         tool_input:str = agent_step.tool_input
    #         observation:int = tool_to_use.func(str(tool_input))
    #         print(f"obervation: {observation=}")
    #         intermediate_steps.append((agent_step, str(observation))

    ### ============================================================================== ###
    ###                  save the result to a directly executable file                 ###
    ### ============================================================================== ###
    gen_model_filename = os.path.join(rules_dir, "llm_gen/coin_new_model.pl")
    with open(gen_model_filename, 'w') as gen_f:
        gen_f.write(agent_step[0])