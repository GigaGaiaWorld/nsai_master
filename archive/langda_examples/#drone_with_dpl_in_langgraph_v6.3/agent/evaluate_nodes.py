from typing import List, Any, Type, Tuple
from agent.requirements_builder import RequirementsBuilder
from utils import (
    _find_all_blocks, 
    _replace_placeholder, 
    invoke_agent,
    _parse_simple_dictonary,
)
from state import BasicState, TaskStatus
from config import paths
from problog.program import PrologString
from problog import get_evaluatable, evaluator
import traceback
import logging
logger = logging.getLogger(__name__)

class EvaluateNodes:
    """
    The nodes that are used for testing results
    """

    @staticmethod
    def test_node(state:BasicState):
        print("processing test_node...")
        state["status"] = TaskStatus.TEST
        regenerate_info:List[str] = []
        test_prompt_template = _replace_placeholder(state["prompt_template"],state["generated_codes"])
        constructed_code_list = RequirementsBuilder.build_report_info(state["generated_codes"],state["langda_dicts"])

        if state["has_query"]: # need to do a test first
            input={
                "test_result": EvaluateNodes.problog_test_tool(test_prompt_template),
                "output": test_prompt_template,
                "code_list":"\n".join(constructed_code_list),
            }
        else:
            input={
                "output": test_prompt_template,
                "code_list":"\n".join(constructed_code_list),
            }
        constructed_code_list = RequirementsBuilder.build_report_info(state["generated_codes"],state["langda_dicts"])

        evaluated_result,formatted_prompt = invoke_agent(
            react=state["usereact"], 
            model_name=state["model_name"], 
            tools=["search_tool","retriever_tool","problog_test_tool"], 
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
        elif state["iter_count"] >= 5:
            logger.warning("Exceed the maximum iterate limitation.")
            return "summary_node"
        else:
            return "generate_node"
        
    @staticmethod
    def problog_test_tool(model: str) -> Tuple[str,bool]:
        """Run the Problog evaluation tool."""
        try:
            result = []
            evaluatable:Type[evaluator.Evaluatable] = get_evaluatable().create_from(PrologString(model))
            results:(dict | Any) = evaluatable.evaluate()
            
            for query_key, probability in results.items():
                result_line = f"{query_key} = {probability:.4f}"
                result.append(result_line)
            result_lines = "% Problog Inference Result：\n" + "\n".join(result)
            print(result_lines)
            return result_lines
        except Exception:
            tb_lines = traceback.format_exc().splitlines()
            last_five = tb_lines[-5:]
            error_message = "Error evaluating Problog model:\n" + "\n".join(last_five)
            print(error_message)
            return error_message