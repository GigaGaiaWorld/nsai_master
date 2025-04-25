import time
from utils import _replace_placeholder
from typing import TypedDict, List, Dict
from agent.requirements_builder import RequirementsBuilder
from utils import (
    _replace_placeholder, 
    integrated_code_parser,
    _parse_simple_dictonary,
    _list_to_dict
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
        fest_codes:List[str] = []
        langda_dicts:List[LangdaDict] = []
        requirements:Dict[list] = {}

        raw_prompt_template, lann_dicts, raw_langda_dicts = integrated_code_parser(state["rule_string"])
        paths.save_as_file(raw_prompt_template,"prompt_template","1st")

        with DictDB() as langdaDB:
            for idx, langda in enumerate(raw_langda_dicts):
                if langda["FUP"]:
                    fest_codes.append(None)
                    langda_dicts.append(langda)
                else:
                    code = langdaDB.get_item(langda["HASH"])
                    fest_codes.append(code)
                    if not code: 
                        langda_dicts.append(langda)

        prompt_template = _replace_placeholder(raw_prompt_template,fest_codes,state["placeholder"])
        if lann_dicts:
            requirements["LANN"]=RequirementsBuilder.build_all_network_info(lann_dicts)
        else:
            requirements["LANN"] = []
        requirements["LANGDA"] = RequirementsBuilder.build_all_langda_info(langda_dicts)

        requirements_str = "\n".join(requirements)
        paths.save_as_file(requirements_str,"prompt_template","req")
        return {"prompt_template":prompt_template,             # the string that only leave needed "{LANGDA}" slot for prompting
                "lann_dicts":lann_dicts,                        # the dict that contains detail informations about network
                "langda_dicts":langda_dicts,                    # the dict that contains detail informations about langda
                "requirements":requirements,                    # 
        }

    @staticmethod
    def summary_node(state:BasicState):
        """
        summary...
        """
        print("processing summary_node...")
        final_code = _replace_placeholder(state["prompt_template"],state["fest_codes"], state["placeholder"])
        paths.save_as_file(final_code,"final_code")

        fest_dict = _list_to_dict(state["fest_codes"])
        with DictDB() as langdaDB:
            langdaDB.sync_with_dict(fest_dict)

        state["endtime"] = time.time()
        running_time = round(state["endtime"]-state["srttime"])
        print("running_time",running_time)
        print("total round:",state["iter_count"])
        # some other summaries...

        return state