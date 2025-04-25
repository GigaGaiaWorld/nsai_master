from typing import List, Dict
from agent.requirements_builder import RequirementsBuilder
from utils import (
    _find_all_blocks, 
    _replace_placeholder, 
    invoke_agent,
    _parse_simple_dictonary
)
from state import BasicState, TaskStatus
from config import paths

class EvaluateNodes:
    """
    The nodes that are used for testing results
    """

    @staticmethod
    def test_node(state:BasicState):
        print("processing test_node...")
        state["status"] = TaskStatus.TEST
        regenerate_info:List[str] = []

        constructed_code_list = RequirementsBuilder.build_report_info(state["generated_codes"])
        input={
            "error_report": state["error_report"],
            "context": state["user_context"],
            "output": state["final_code"],
            "code_list":"\n".join(constructed_code_list),
        }

        evaluated_result = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type="evaluate", 
            input=input, 
            config=state["config"])

        paths.save_as_file(evaluated_result, "evaluated_result",state["iter_count"])

        evaluated_codes = _find_all_blocks("report",evaluated_result) # [{report:"",need_regenerate:"True"},...]

        origin_fest_codes = state["fest_codes"]
        fest_codes, regenerate_info = RequirementsBuilder.build_regenerate_info(state["generated_codes"],evaluated_codes,state["requirements"])

        iter = 0
        for i, fest_item in enumerate(origin_fest_codes):
            key, value = _parse_simple_dictonary(fest_item)
            if not value:
                new_key, new_value = _parse_simple_dictonary(fest_codes[iter])
                if new_key != key:
                    raise ValueError("regenerate_node: the hash of generated code doesn't match!")
            origin_fest_codes[i][key] = new_value
            iter += 1

        if evaluated_codes:
            return {
                "fest_codes":origin_fest_codes,
                "evaluated_result":evaluated_result,
                "evaluated_codes":evaluated_codes,
                "regenerate_info":regenerate_info,
                }
        else:
            raise ValueError("test_node: Generated report no found...")

    @staticmethod
    def _decide_next(state:BasicState):
        print("processing _decide_next...")
        print("#current round:",state["iter_count"])
        to_end = True
        for fest_code in state["fest_codes"]:
            key, value = _parse_simple_dictonary(fest_code)
            if value == None:
                to_end = False
        if to_end or state["iter_count"] >= 3:
            state["status"] = TaskStatus.CMPL
            return "summary_node"
        else:
            return "generate_node"

    # @staticmethod
    # def regenerate_node(state:BasicState):
    #     """
    #     Regenerate specific code blocks based on evaluation.
    #     """
    #     print("processing regenerate_node...")
    #     state["status"] = TaskStatus.GNRT
    #     new_iter_count = state["iter_count"] + 1

    #     new_fest_code = [] # the codes that does not to regenerate
    #     code_with_report_list = []
    #     regenerate_indices = []

    #     new_fest_code, code_with_report_list, regenerate_indices = RequirementsBuilder.build_regenerate_info(state["generated_codes"],state["evaluated_codes"])

    #     # Prepare input for the regeneration prompt
    #     regenerate_template = _replace_placeholder(state["prompt_template"],new_fest_code, "{{LANGDA}}")
    #     print("=====================regenerate_template=====================\n",regenerate_template,"\n=============================================================\n")
    #     input={
    #         "context": state["user_context"],
    #         "rule_set": regenerate_template,
    #         "blocks_with_analysis":"\n".join(code_with_report_list),
    #     }
    #     # Run the regeneration
    #     # regenerated_result = self.executor.invoke_agent("regenerate",input,self.config)
    #     regenerated_result = invoke_agent(
    #         react=False, 
    #         model_name=state["model_name"], 
    #         tools=state["tools"], 
    #         prompt_type="regenerate", 
    #         input=input, 
    #         config=state["config"])

    #     paths.save_as_file(regenerated_result,"generated_result",state["iter_count"])

    #     # Extract the regenerated code blocks
    #     regenerated_codes = _find_all_blocks('code',regenerated_result)
    #     print("=====================regenerated_codes=====================\n",regenerated_codes,"\n=============================================================\nregenerate_indices:",regenerate_indices)
    #     if len(regenerated_codes) != len(regenerate_indices):
    #         raise ValueError("The amount of code generated does not matches the number of code blocks that need to be regenerated")

    #     paths.save_as_file(regenerated_codes,"generated_codes","re")
    #     paths.save_as_file(code_with_report_list,"evaluated_codes","&code")

    #     return {
    #         "generated_codes":regenerated_codes,
    #         "prompt_template":regenerate_template, 
    #         "new_iter_count":new_iter_count,
    #     }
        