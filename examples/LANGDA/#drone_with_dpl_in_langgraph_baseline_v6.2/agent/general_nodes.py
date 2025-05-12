import time
from typing import TypedDict, List, Dict
from agent.requirements_builder import RequirementsBuilder

from utils import (
    integrated_code_parser,
    _parse_simple_dictonary,
    invoke_agent,
    _find_all_blocks,
    _replace_placeholder
)
from state import BasicState, TaskStatus
from config import paths
from database import DictDB

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
        print("processing parse_node...")
        state["status"] = TaskStatus.INIT
        fest_codes:List[dict] = []      # {"hash1":"code1","hash2":"code2",...}
        langda_dicts:List[LangdaDict] = []

        raw_prompt_template, lann_dicts, raw_langda_dicts = integrated_code_parser(state["rule_string"])

        with DictDB() as langdaDB:
            for idx, langda in enumerate(raw_langda_dicts):
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
        # paths.save_as_file(langda_dicts,"prompt",f"{state['prefix']}/langda_dict")

        langda_reqs, lann_reqs  = RequirementsBuilder.build_requirements(lann_dicts, langda_dicts)

        return {"prompt_template":raw_prompt_template,             # the string that only leave needed "{LANGDA}" slot for prompting
                "lann_dicts":lann_dicts,                        # the dict that contains detail informations about network
                "langda_dicts":langda_dicts,                    # the dict that contains detail informations about langda
                "lann_reqs":lann_reqs,                    # 
                "langda_reqs":langda_reqs,                    # 
                "fest_codes":fest_codes, 
        }


    @staticmethod
    def generate_baseline_natural_node(state:BasicState):
        """
        raw langda file, all langda terms are replaced with natural language
        result as whole file
        """
        replace_natural_language = []
        for langda_dict in state["langda_dicts"]:
            replace_natural_language.append(langda_dict["LLM"])
        prompt_template = _replace_placeholder(state["prompt_template"], replace_natural_language, state["placeholder"])

        input={
            "context": state["user_context"],
            "rule_set": prompt_template,
        }

        generated_result, formatted_prompt = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type="baseline_skeleton", 
            input=input, 
            config=state["config"])
        paths.save_as_file(formatted_prompt,"prompt",f"prompt/{state['prefix']}")
        return {
            "generated_codes":generated_result,           # [{"hash1":"code block1"}, {"hash2":"code block2"}, ...]
        }
    
    @staticmethod
    def generate_baseline_skeleton_node(state:BasicState):
        """
        raw langda file, no modification
        result as whole file
        """

        input={
            "context": state["user_context"],
            "rule_set": state["rule_string"],
        }

        generated_result, formatted_prompt = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type="baseline_skeleton", 
            input=input, 
            config=state["config"])
        return {
            "generated_codes":generated_result,           # [{"hash1":"code block1"}, {"hash2":"code block2"}, ...]
        }

    @staticmethod
    def generate_baseline_requires_node(state:BasicState):
        """
        file with placeholder, use build_generate_info
        result as whole file
        """
        requirement_input = "\n".join(RequirementsBuilder.build_generate_info(state["langda_reqs"],state["lann_reqs"]))
        input={
            "context": state["user_context"],
            "rule_set": state["prompt_template"],
            "requirements": requirement_input,
        }

        generated_result, formatted_prompt = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type="baseline_requires", 
            input=input, 
            config=state["config"])
        return {
            "generated_codes":generated_result,           # [{"hash1":"code block1"}, {"hash2":"code block2"}, ...]
        }

    @staticmethod
    def generate_baseline_full_node(state:BasicState):
        """
        file with placeholder, use build_generate_info
        result as whole file
        """
        requirement_input = "\n".join(RequirementsBuilder.build_generate_info(state["langda_reqs"],state["lann_reqs"]))
        input={
            "context": state["user_context"],
            "rule_set": state["rule_string"],
            "requirements": requirement_input,
        }
        generated_result, formatted_prompt = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type="baseline_full", 
            input=input, 
            config=state["config"])
        return {
            "generated_codes":generated_result,           # [{"hash1":"code block1"}, {"hash2":"code block2"}, ...]
        }
    @staticmethod
    def summary_node(state:BasicState):
        """
        summary...
        """
        print("processing summary_node...")
        state["status"] = TaskStatus.CMPL

        # final_code = _replace_placeholder(state["prompt_template"],state["fest_codes"], state["placeholder"])
        # final_code = _find_all_blocks("code",state["generated_codes"])
        # _, value_code = _parse_simple_dictonary(final_code[0])

        input={
            "original_ruleset": state["rule_string"],
            "generated_ruleset": state["generated_codes"],
        }
        final_result, _  = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type="final_test", 
            input=input, 
            config=state["config"])

        final_dict = _find_all_blocks("other",final_result, state['prefix'])
        _, value = _parse_simple_dictonary(final_dict[0])
        validity = value["Valid"]
        final_report = value["Report"]
        paths.save_as_file(state["generated_codes"],"final_code",f"final/{state['prefix']}")
        # paths.save_as_file("Validity:\n"+validity+"\n\nReport:\n"+final_report,"result",f"final/{state['prefix']}")
        paths.save_as_file(final_report,"result",f"final/{state['prefix']}")

        # fest_dict = _list_to_dict(state["fest_codes"])
        # with DictDB() as langdaDB:
        #     langdaDB.sync_with_dict(fest_dict)

        state["endtime"] = time.time()
        # running_time = round(state["endtime"]-state["srttime"])
        # print("total round:",state["iter_count"])
        # some other summaries...

        return state
    
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
        
    # @staticmethod
    # def _final_test_node(state:BasicState):
