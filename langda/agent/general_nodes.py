import re
import time
from typing import TypedDict, List, Dict
from .requirements_builder import RequirementsBuilder
from ..utils import (
    _replace_placeholder, 
    integrated_code_parser,
    _parse_simple_dictonary,
    problog_test_tool,
    _list_to_dict,
)
from .state import BasicState, TaskStatus
from ..config import paths
from ..database import DictDB
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
            print(langdaDB.get_all_items())

            for idx, langda in enumerate(raw_langda_dicts):
                """ 
                The timing of replacing the new message is at init time, so that the HASH of the code 
                will be determined according to the previous mark tag. Later, when the code is run but not updated, 
                it can be ensured that the previous code content is automatically extracted from the database.
                """
                if state["langda_ext"]: # If has "dynamic content": for example /* Secure */, parse the content
                    langda_ext_dict = state["langda_ext"]
                    for raw_langda_dict in raw_langda_dicts:
                        langda_ext_pattern = r'/\*\s*(\w+)\s*\*/'
                        ext_match = re.search(langda_ext_pattern, raw_langda_dict["LLM"])
                        if ext_match:
                            try:
                                raw_langda_dict["LLM"] = langda_ext_dict[ext_match[1]]
                                print("prompt from external received:",langda_ext_dict[ext_match[1]])
                            except:
                                print("The external message is incorrect or there's unfullfilled /* Code */ in langda code...")
                                raise ValueError("The external message is incorrect or there's unfullfilled /* Code */ in langda code...")
                            
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
        print(fest_codes)
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
            sync_dict = _list_to_dict(state["temp_full_codes"])
        except: # if there's no langda term and jump to this node directly
            final_code = _replace_placeholder(state["prompt_template"],state["fest_codes"], state["placeholder"])
            sync_dict = _list_to_dict(state["fest_codes"])
        print("*** test_result: ***\n")
        result_new = problog_test_tool(final_code,state["prefix"],timeout = 120)

        # Don't delete! Database part!
        with DictDB() as langdaDB:
            langdaDB.sync_with_dict(sync_dict)
            print(langdaDB.get_all_items())

        # paths.save_as_file(final_code + f"\n\n*** Result:*** \n{result_new} \n\n***Report:***\nValidity_form:{Validity_form}\Validity_result:{Validity_result}\n{final_report}","final_code",f"test_history/_final/{state['prefix']}")
        paths.save_as_file(final_code + f"\n\n%%% Result %%% \n{result_new}","final_code",f"test_history/_final/{state['prefix']}")
        # ================== THIS IS ONLY FOR TESTING ================== #

        state["endtime"] = time.time()
        running_time = round(state["endtime"]-state["srttime"])

        # print(f"*** Result:{Validity_form}|{Validity_result}.")
        print(f"*** Running_time: {running_time}s, {state['iter_count']} rounds in total.")
        # some other summaries...

        return {
            "final_result":{
                "final_result":final_code,
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