from typing import List
from agent.requirements_builder import RequirementsBuilder
from utils import (
    _find_all_blocks, 
    _replace_placeholder, 
    invoke_agent,
    _parse_simple_dictonary,
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
        test_prompt_template = _replace_placeholder(state["prompt_template"],state["fest_codes"])
        constructed_code_list = RequirementsBuilder.build_report_info(state["generated_codes"],state["langda_dicts"])
        input={
            "error_report": state["error_report"],
            "context": state["user_context"],
            "output": test_prompt_template,
            "code_list":"\n".join(constructed_code_list),
        }

        evaluated_result,formatted_prompt  = invoke_agent(
            react=False, 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type="evaluate", 
            input=input, 
            config=state["config"])
        
        paths.save_as_file(formatted_prompt,"prompt",f"{state['prefix']}/formatted_evaluate")
        paths.save_as_file(evaluated_result, "result",f"{state['prefix']}/#eval_{state['iter_count']}")

        origin_fest_codes = state["fest_codes"]
        evaluated_codes = _find_all_blocks("report",evaluated_result) # [{report:"",need_regenerate:"True"},...]

        new_fest_codes, regenerate_info = RequirementsBuilder.build_regenerate_info(
            state["generated_codes"],
            evaluated_codes, 
            state["langda_reqs"],
            state["lann_reqs"])

        iter = 0
        for i, fest_item in enumerate(origin_fest_codes):
            key, value = _parse_simple_dictonary(fest_item)
            if not value:
                key_new, value_new = _parse_simple_dictonary(new_fest_codes[iter])
                if not key == key_new:
                    raise ValueError(f"test_node: Key '{key}' doesn't match in {new_fest_codes[iter]}.")
                
                origin_fest_codes[i][key] = value_new
                iter += 1

        if evaluated_codes:
            return {
                "fest_codes":origin_fest_codes,
                "regenerate_info":regenerate_info,
            }
        else:
            raise ValueError("test_node: Generated report no found...")

    @staticmethod
    def _decide_next_eval(state:BasicState):
        print("processing _decide_next_eval... #current round:",state["iter_count"])

        to_end = True
        for fest_code in state["fest_codes"]:
            _, value = _parse_simple_dictonary(fest_code)
            if value == None:
                to_end = False
        if to_end:
            return "summary_node"
        elif state["iter_count"] >= 5:
            raise ValueError("Exceed the maximum iterate limitation.")
        else:
            return "generate_node"
        

