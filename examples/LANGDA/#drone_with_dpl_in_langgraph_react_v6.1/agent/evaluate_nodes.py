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
        origin_fest_codes = state["fest_codes"]
        test_prompt_template = _replace_placeholder(state["prompt_template"],state["fest_codes"])
        constructed_code_list = RequirementsBuilder.build_report_info(state["generated_codes"])
        input={
            "error_report": state["error_report"],
            "context": state["user_context"],
            "output": test_prompt_template,
            "code_list":"\n".join(constructed_code_list),
        }

        evaluated_result = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type="evaluate", 
            input=input, 
            config=state["config"])

        paths.save_as_file(evaluated_result, "result",f"eval_{state['iter_count']}")

        evaluated_codes = _find_all_blocks("report",evaluated_result) # [{report:"",need_regenerate:"True"},...]

        fest_codes, regenerate_info = RequirementsBuilder.build_regenerate_info(state["generated_codes"],evaluated_codes,state["langda_reqs"],state["lann_reqs"])

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
                # "evaluated_result":evaluated_result,
                # "evaluated_codes":evaluated_codes,
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
            return "summary_node"
        else:
            return "generate_node"