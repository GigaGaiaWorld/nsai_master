import signal
from problog.program import PrologString
from problog import get_evaluatable, evaluator
from typing import Any, Type, Tuple, Callable
import traceback
import multiprocessing as mp
# Run workflow with timeout mechanism:
def with_timeout(func, file_basename, timeout=120, *args, **kwargs):
    """
    args:
        func: input main workflow function: agent.call_langda_workflow
        file_basename: current file name
        timeout: timeout for timeout_handler
    """
    # Define the alarm handler function
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Function timed out while processing file: {file_basename}")
    # Setting up the signal processor:
    signal.signal(signal.SIGALRM, timeout_handler) # TSIGALRM: imer signal from alarm(2).  
    signal.alarm(timeout)  # Set timeout

    try:
        result = func(*args, **kwargs)
        signal.alarm(0)  # Close the alarm
        return result
    except TimeoutError as e:
        return f"ERROR: Execution timed out after {timeout} seconds"
    finally:
        signal.alarm(0)  # Ensure to close the alarm

# def target(func,return_dict:dict,*args, **kwargs):
#     try:
#         result = func(*args, **kwargs)
#         return_dict["result"] = result
#     except Exception as e:
#         return_dict["result"] = str(e)

# def with_timeout(func:Callable, file_basename, timeout=60, *args, **kwargs):

#     return_dict = mp.Manager().dict()
#     reasoning_process = mp.Process(target=target, args=(func,return_dict, args, kwargs,))
#     reasoning_process.start()
#     reasoning_process.join(timeout=timeout + 0.01)

#     if reasoning_process.is_alive():
#         reasoning_process.terminate()
#         reasoning_process.join(timeout=3.0)
#         if reasoning_process.is_alive():
#             reasoning_process.kill()
#             reasoning_process.join()
#         return f"ERROR: File {file_basename}: Execution timed out after {timeout} seconds"
#     try:
#         return return_dict["result"]
#     except:
#         return "ERROR: File {file_basename}: Process ended without result"
    
def _problog_test(model: str) -> Tuple[str,bool]:
    """Run the Problog evaluation tool."""
    print("""Running problog_test_tool...""")
    try:
        result = []
        evaluatable:Type[evaluator.Evaluatable] = get_evaluatable().create_from(PrologString(model))
        results:(dict | Any) = evaluatable.evaluate()

        for query_key, probability in results.items():
            result_line = f"{query_key} = {probability:.4f}"
            result.append(result_line)
            
        if len(result) > 20:
            result_lines = "% Problog Inference Result：\n" + "\n".join(result[:20]) + "\n ...<other results>... "
        else:
            result_lines = "% Problog Inference Result：\n" + "\n".join(result)
        print(" ------------- result_lines ------------- \n" + "\n".join(result[:5]))
        return result_lines
    except Exception:
        tb_lines = traceback.format_exc().splitlines()
        last_five = tb_lines[-5:]
        error_message = "Error evaluating Problog model:\n" + "\n".join(last_five)
        print(error_message)
        return error_message
    
