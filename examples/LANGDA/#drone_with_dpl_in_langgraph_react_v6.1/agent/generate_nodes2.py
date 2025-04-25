from typing import List, Dict
from .requirements_builder import RequirementsBuilder
from utils import _find_all_blocks, integrated_code_parser, invoke_agent, _compute_short_md5
from state import BasicState, TaskStatus
from config import paths
from database import DictDB

class GenerateNodes:
    """
    The nodes that are used for generating code
        there are THREE special terms that defined in langda predicate:
        LOT:"list of tools that it could use"
        NET:"description about how it should work with certain network"
        LLM:"some natural language descriptions that describs requirements"
        they won't show up in final langda predicate, and only used to construct the deepproblog code.
    """

    @staticmethod
    def parse_node(state:BasicState):
        """
        parsing the original deepproblog string
        return:
            prompt_template: all langda terms are replaced with placeholder
            lann_dicts: lann informations
            langda_dicts: langda informations
        """
        print("processing parse_node...")
        prompt_template, lann_dicts, langda_dicts = integrated_code_parser(state["rule_string"])
        paths.save_as_file(prompt_template,"prompt_template","1st")

        return {"prompt_template":"\n".join(prompt_template),     # the string that only leave "{LANGDA}" slot for prompting
                "lann_dicts":lann_dicts,                        # the dict that contains detail informations about network
                "langda_dicts":langda_dicts}                     # the dict that contains detail informations about langda

    @staticmethod
    def requirements_node(state:BasicState):
        """
        fixed beautiful version, the main logics are written in RequirementsBuilder
        return:
            it will add prompt_requirements to state
        """
        print("processing requirements_node...")

        lann_dict:Dict[str,dict] = state["lann_dicts"]
        langda_dict:Dict[str,dict] = state["langda_dicts"]


        # Construct the requirement part of prompt:
        if lann_dicts:
            requirements=RequirementsBuilder.build_network_info(lann_dicts)
            requirements.append(RequirementsBuilder.build_langda_info(langda_dicts))
        else:
            requirements = RequirementsBuilder.build_langda_info(langda_dicts)

        requirements_str = "\n".join(requirements)
        paths.save_as_file(requirements_str,"prompt_template","req")

        return{
            "prompt_requirements":requirements_str,
        }

    @staticmethod
    def generate_node(state:BasicState):
        """
        generate the code, the core of the wor
        return:
            it will add generated_codes to state, and the iter_count will add one
        """
        print("processing generate_node...")
        langdaDB = DictDB()

        new_iter_count = state["iter_count"] + 1
        state["status"] = TaskStatus.GNRT

        input={
            "context": state["user_context"],
            "requirements": state["prompt_requirements"],
            "rule_set":state["prompt_template"],
        }

        result = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type="generate", 
            input=input, 
            config=state["config"])

        paths.save_as_file(result,"generated_result")

        generated_codes = _find_all_blocks("code",result)

        langdaDB.sync_with_dict()




        langdaDB.close()
        if generated_codes:
            return {
                "iter_count": new_iter_count,
                "generated_codes":generated_codes
            }
        else:
            raise ValueError("generate_node: Generated code no found...")