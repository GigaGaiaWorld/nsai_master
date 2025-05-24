import re
import time
from utils import _replace_placeholder
from typing import TypedDict, List, Dict
from agent.requirements_builder import RequirementsBuilder
from utils import (
    _replace_placeholder, 
    integrated_code_parser,
    _parse_simple_dictonary,
    invoke_agent,
    _find_all_blocks,
    problog_test_tool,
)
from agent.state import BasicState, TaskStatus
from config import paths
from database import DictDB
from typing import List, Any, Type, Tuple

class LangdaDict(TypedDict):
    HEAD: str
    HASH: str

    LOT: str
    NET: str
    LLM: str
    FUP: str

class GeneralNodes:
    """
    The nodes that are used for general perpose
    """

    @staticmethod
    def init_node(state:BasicState):
        """
        parsing the original deepproblog string
        return:
            prompt_template: all langda terms are replaced with placeholder
            lann_dicts: lann informations
            langda_dicts: langda informations
        """
        print("### =========== processing init_node =========== ###")
        state["status"] = TaskStatus.INIT
        fest_codes:List[dict] = []      # {"hash1":"code1","hash2":"code2",...}
        langda_dicts:List[LangdaDict] = []

        raw_prompt_template, lann_dicts, raw_langda_dicts, has_query = integrated_code_parser(state["rule_string"])
        with DictDB() as langdaDB:
            for idx, langda in enumerate(raw_langda_dicts):
                """ 
                The timing of replacing the new message is at init time, so that the HASH of the code 
                will be determined according to the previous mark tag. Later, when the code is run but not updated, 
                it can be ensured that the previous code content is automatically extracted from the database.
                """
                if state["langda_ext"]:
                    langda_ext_dict = state["langda_ext"]
                    for raw_langda_dict in raw_langda_dicts:
                        langda_ext_pattern = r'/\*\s*(\w+)\s*\*/'
                        ext_match = re.search(langda_ext_pattern, raw_langda_dict["LLM"])
                        if ext_match:
                            print("ext_match",ext_match[1])

                            try:
                                raw_langda_dict["LLM"] = langda_ext_dict[ext_match[1]]
                                print("raw_langda_dict[LLM]",raw_langda_dict["LLM"])
                                print("langda_ext_dict[ext_match]",langda_ext_dict[ext_match[1]])

                            except:
                                print("The message from telegram is incorrect or there's unfullfilled /* Code */ in langda code...")
                                raise ValueError("The message from telegram is incorrect or there's unfullfilled /* Code */ in langda code...")
                            
                if langda["FUP"] == "True" or langda["FUP"] == "true" or langda["FUP"] == "T":
                    fest_codes.append({langda["HASH"]:None})
                    langda_dicts.append(langda)
                elif langda["FUP"] == "False" or langda["FUP"] == "false" or langda["FUP"] == "F":
                    code = langdaDB.get_item(langda["HASH"])
                    fest_codes.append({langda["HASH"]:code})
                    if not code: 
                        langda_dicts.append(langda)
                else:
                    raise ValueError("The value of FUP term should be one of [True,true,T,False,false,F]")   
        paths.save_as_file(langda_dicts,"prompt",f"test_history/{state['prefix']}/langda_dict")

        langda_reqs  = RequirementsBuilder.build_all_langda_info(langda_dicts)
        return {"prompt_template":raw_prompt_template,             # the string that only leave needed "{LANGDA}" slot for prompting
                # "lann_dicts":lann_dicts,                        # the dict that contains detail informations about network
                "langda_dicts":langda_dicts,                    # the dict that contains detail informations about langda
                # "lann_reqs":lann_reqs,                    # 
                "langda_reqs":langda_reqs,                    # 
                "fest_codes":fest_codes, 
                "has_query":has_query,
        }

    @staticmethod
    def summary_node(state:BasicState):
        """
        summary...
        """
        print("### =========== processing summary_node =========== ###")
        state["status"] = TaskStatus.CMPL
        state["endtime"] = time.time()
        try: 
            final_code = _replace_placeholder(state["prompt_template"],state["temp_full_codes"], state["placeholder"])
        except: # if there's no langda term and jump to this node directly
            final_code = _replace_placeholder(state["prompt_template"],state["fest_codes"], state["placeholder"])
        # Don't delete this! Use "fest_codes" version
        # final_code = _replace_placeholder(state["prompt_template"],state["fest_codes"], state["placeholder"])

        # ================== THIS IS ONLY FOR TESTING ================== #
        print("*** test_answer: ***\n")
        result_origin = problog_test_tool(state["true_string"],state["prefix"],timeout = 120)
        print("*** test_result: ***\n")
        result_new = problog_test_tool(final_code,state["prefix"],timeout = 120)
        input={
            "original_ruleset": state["true_string"],
            "original_result": result_origin,
            "generated_ruleset": final_code,
            "generated_result": result_new,
            "test_analysis": [], # no need to analysis any detailed rules
        }
        final_result, _, _  = invoke_agent(
            agent_type="simple", 
            model_name=state["model_name"], 
            tools=[], 
            prompt_type="final_test", 
            input=input,
            config=state["config"])
        final_dict = (_find_all_blocks("final",final_result))[0]
        Validity_form = final_dict["Validity_form"]
        Validity_result = final_dict["Validity_result"]
        final_report = final_dict["Report"]

        # Don't delete! Database part!
        # fest_dict = _list_to_dict(state["fest_codes"])
        # with DictDB() as langdaDB:
        #     langdaDB.sync_with_dict(fest_dict)

        paths.save_as_file(final_code + f"\n\n*** Result:*** \n{result_new} \n\n***Report:***\nValidity_form:{Validity_form}\Validity_result:{Validity_result}\n{final_report}","final_code",f"test_history/_final/{state['prefix']}")
        # ================== THIS IS ONLY FOR TESTING ================== #

        state["endtime"] = time.time()
        running_time = round(state["endtime"]-state["srttime"])

        print(f"*** Result:{Validity_form}|{Validity_result}.")
        print(f"*** Running_time: {running_time}s, {state['iter_count']} rounds in total.")
        # some other summaries...

        return {
            "final_result":{
                "Validity_form":Validity_form,
                "Validity_result":Validity_result,
                "final_report":final_report,
                "final_result":result_new,
                "running_time":running_time,
                "iter_count":state["iter_count"],
            }
        }

    @staticmethod
    def _decide_next_init(state:BasicState):
        print("processing _decide_next_init ...")
        count_need_generated = 0
        for fest_code in state["fest_codes"]:
            _, value = _parse_simple_dictonary(fest_code)
            if value == None:
                count_need_generated += 1

        if not(count_need_generated > 0):
            state["error_report"] = "No langda needs to be updated"
            print(f"{state['error_report']}, process end now...")

            return "summary_node"
        else:
            return "generate_node"
        


    @staticmethod
    def baseline_node(state:BasicState):
        final_code = ""
        input={
            "prompt_template": "",   # code with <langda>
            "constructed_code": "", # full code
            "test_analysis": state["test_analysis"], # analysis
        }
        generated_result,_,_  = invoke_agent(
            agent_type="baseline", 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type=state["rule_string"], 
            input=input, 
            config=state["config"])
        
        pattern = r"```(?:problog|[a-z]*)?\n(.*?)```"
        matches = re.findall(pattern, generated_result, re.DOTALL)
        for match in matches:
            final_code += match
            final_code += "\n\n"

        # ================== THIS IS ONLY FOR TESTING ================== #
        print("*** test_answer: ***\n")
        result_origin = problog_test_tool(state["true_string"],state["prefix"],timeout = 120)
        print("*** test_result: ***\n")
        result_new = problog_test_tool(final_code,state["prefix"],timeout = 120)
        input={
            "original_ruleset": state["true_string"],
            "original_result": result_origin,
            "generated_ruleset": final_code,
            "generated_result": result_new,
            "test_analysis": [], # no need to analysis any detailed rules
        }
        final_result, _, _  = invoke_agent(
            agent_type="simple", 
            model_name=state["model_name"], 
            tools=[], 
            prompt_type="final_test", 
            input=input,
            config=state["config"])

        final_dict = (_find_all_blocks("final",final_result))[0]
        Validity_form = final_dict["Validity_form"]
        Validity_result = final_dict["Validity_result"]
        final_report = final_dict["Report"]

        # Don't delete! Database part!
        # fest_dict = _list_to_dict(state["fest_codes"])
        # with DictDB() as langdaDB:
        #     langdaDB.sync_with_dict(fest_dict)

        paths.save_as_file(final_code + f"\n\n*** Result:*** \n{result_new} \n\n***Report:***\nValidity_form:{Validity_form}\Validity_result:{Validity_result}\n{final_report}","final_code",f"test_history/_final/{state['prefix']}")
        # ================== THIS IS ONLY FOR TESTING ================== #

        state["endtime"] = time.time()
        running_time = round(state["endtime"]-state["srttime"])

        print(f"*** Result:{Validity_form}|{Validity_result}.")
        print(f"*** Running_time: {running_time}s, {state['iter_count']} rounds in total.")
        # some other summaries...

        return {
            "final_result":{
                "Validity_form":Validity_form,
                "Validity_result":Validity_result,
                "final_report":final_report,
                "final_result":result_new,
                "running_time":running_time,
                "iter_count":state["iter_count"],
            }
        }