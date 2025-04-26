import time
from utils import _replace_placeholder
from typing import TypedDict, List, Dict
from agent.requirements_builder import RequirementsBuilder
from utils import (
    _replace_placeholder, 
    integrated_code_parser,
    _list_to_dict,
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
        fest_codes:List[dict] = []      # {"hash1":"code1","hash2":"code2",...}
        langda_dicts:List[LangdaDict] = []

        raw_prompt_template, lann_dicts, raw_langda_dicts = integrated_code_parser(state["rule_string"])
        paths.save_as_file(raw_prompt_template,"prompt","1st")
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
                    

        prompt_template = _replace_placeholder(raw_prompt_template,fest_codes,state["placeholder"])
        lann_reqs, langda_reqs = RequirementsBuilder.build_requirements(lann_dicts, langda_dicts)
        return {"prompt_template":prompt_template,             # the string that only leave needed "{LANGDA}" slot for prompting
                "lann_dicts":lann_dicts,                        # the dict that contains detail informations about network
                "langda_dicts":langda_dicts,                    # the dict that contains detail informations about langda
                "lann_reqs":lann_reqs,                    # 
                "langda_reqs":langda_reqs,                    # 
                "fest_codes":fest_codes, 
        }

    @staticmethod
    def summary_node(state:BasicState):
        """
        summary...
        """
        print("processing summary_node...")
        state["status"] = TaskStatus.CMPL

        final_code = _replace_placeholder(state["prompt_template"],state["fest_codes"], state["placeholder"])
        paths.save_as_file(final_code,"final_code",f"{state['prefix']}")

        fest_dict = _list_to_dict(state["fest_codes"])
        with DictDB() as langdaDB:
            langdaDB.sync_with_dict(fest_dict)

        state["endtime"] = time.time()
        running_time = round(state["endtime"]-state["srttime"])
        print("running_time",running_time)
        print("total round:",state["iter_count"])
        # some other summaries...

        return state