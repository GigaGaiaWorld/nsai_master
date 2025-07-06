from typing import List
from agent.requirements_builder import RequirementsBuilder
from utils import (
    _find_all_blocks, 
    _replace_placeholder, 
    invoke_agent,
    _parse_simple_dictonary,
    problog_test_tool,
)
from agent.state import BasicState, TaskStatus
from config import paths
import logging
logger = logging.getLogger(__name__)

class EvaluateNodes:
    """
    The nodes that are used for testing results
    """

    @staticmethod
    def test_node(state:BasicState):
        print(f"### =========== ### current round: {state['iter_count']} ### =========== ###")
        print("### =========== processing test_node =========== ###")
        state["status"] = TaskStatus.TEST
        test_result:str = ""
        regenerate_info:List[str] = []
        # problog_test_tool:
        constructed_code = _replace_placeholder(state["prompt_template"],state["temp_full_codes"])
        if state["has_query"]: # need to do a test first
            test_result = problog_test_tool(constructed_code,state["prefix"],timeout=60)

        # TEST:
        raw_prompt_template = _replace_placeholder(state["prompt_template"], state["fest_codes"], state["placeholder"])
        test_result_info, report_info = RequirementsBuilder.build_all_report_info(state["generated_codes"],state["langda_dicts"], test_result)
        test_prompt_template = _replace_placeholder(raw_prompt_template, report_info) + "\n" + test_result_info

        input={
            "input": test_prompt_template,
        }

        evaluated_result,formatted_prompt = invoke_agent(
            agent_type=state["agent_type"]["evaluate"], 
            model_name=state["model_name"], 
            tools=state["tools"], 
            prompt_type="evaluate", 
            input=input, 
            config=state["config"])

        paths.save_as_file(formatted_prompt,"prompt",f"test_history/{state['prefix']}/formatted_evaluate")
        paths.save_as_file(evaluated_result, "result",f"test_history/{state['prefix']}/#eval_{state['iter_count']}")

        origin_fest_codes = state["fest_codes"]
        evaluated_codes = _find_all_blocks("report",evaluated_result) # [{report:"",need_regenerate:"True"},...]

        new_fest_codes, regenerate_info = RequirementsBuilder.build_all_regenerate_info(
            state["generated_codes"],
            evaluated_codes, 
            state["langda_dicts"],
        )
        iter = 0
        for i, fest_item in enumerate(origin_fest_codes):
            key, value = _parse_simple_dictonary(fest_item)
            if not value:
                key_new, value_new = _parse_simple_dictonary(new_fest_codes[iter])
                if not key == key_new:
                    logger.warning(f"test_node: Key '{key}' doesn't match in {new_fest_codes[iter]}, set as none")
                    origin_fest_codes[i][key] = None
                else:
                    origin_fest_codes[i][key] = value_new
                iter += 1

        if evaluated_codes:
            return {
                "fest_codes":origin_fest_codes,
                "regenerate_info":regenerate_info,
            }
        else:
            logger.warning(f"test_node: Generated report no found...")
            return {
                "fest_codes":origin_fest_codes,
                "regenerate_info":regenerate_info,
            }


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
        elif state["iter_count"] >= 3:
            logger.warning("Exceed the maximum iterate limitation.")
            return "summary_node"
        else:
            return "generate_node"
        