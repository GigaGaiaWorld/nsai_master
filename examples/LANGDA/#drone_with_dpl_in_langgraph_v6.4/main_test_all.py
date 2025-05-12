import os
import csv
import re
import json
import base64
import time
import signal
import traceback
from tqdm import tqdm
from agent import Langda_Agent
from config import paths

# 定义超时异常
class TimeoutException(Exception):
    pass

# 超时处理函数
def timeout_handler(signum, frame):
    raise TimeoutException("Function timed out")

# 带超时的函数包装器
def with_timeout(func, timeout=60, *args, **kwargs):
    """
    在指定的超时时间内执行函数，如果超时则抛出异常
    """
    # 设置信号处理器
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)  # 设置超时
    
    try:
        result = func(*args, **kwargs)
        signal.alarm(0)  # 关闭警报
        return result
    except TimeoutException as e:
        print(f"Function timed out after {timeout} seconds")
        return f"ERROR: Execution timed out after {timeout} seconds"
    finally:
        signal.alarm(0)  # 确保警报被关闭

def process_all_prompt_files_json(test_directory_path, answer_directory_path, model_name, addition_input, output_json_path, timeout=300):
    all_results = []
    
    # Find all prompt files
    prompt_files = []
    for root, _, files in os.walk(test_directory_path):
        for file in files:
            prompt_files.append(os.path.join(root, file))
    
    # 显示总文件数
    total_files = len(prompt_files)
    print(f"Found {total_files} files to process")
    
    # 创建进度条
    pbar = tqdm(total=total_files, desc="Processing files")
    
    # 记录总体开始时间
    total_start_time = time.time()
    
    # Process each prompt file
    for idx, prompt_file in enumerate(prompt_files, 1):
        file_basename = os.path.basename(prompt_file)
        pbar.set_description(f"Processing {file_basename} [{idx}/{total_files}]")
        
        # Extract 10-character type code from filename using regex
        type_match = re.match(r'([A-Za-z0-9]{10}):', file_basename)
        if not type_match:
            print(f"Warning: Could not extract type code from {file_basename}, skipping")
            pbar.update(1)
            continue
        
        type_chars = type_match.group(1)
        
        # Find corresponding answer file
        answer_file = None
        for root, _, files in os.walk(answer_directory_path):
            for file in files:
                if file.startswith(type_chars):
                    answer_file = os.path.join(root, file)
                    break
            if answer_file:
                break
        
        if not answer_file:
            print(f"Warning: No matching answer file found for type code {type_chars}, skipping")
            pbar.update(1)
            continue
        
        # Read answer file for comparison (true_string)
        try:
            with open(answer_file, "r") as f:
                true_string = f.read()
        except Exception as e:
            print(f"Error reading answer file {answer_file}: {str(e)}")
            pbar.update(1)
            continue
        
        # Read the rules from the prompt file
        try:
            with open(prompt_file, "r") as f:
                rules_string = f.read()
        except Exception as e:
            print(f"Error reading prompt file {prompt_file}: {str(e)}")
            pbar.update(1)
            continue
        
        # Update the prefix in addition_input
        file_specific_input = addition_input.copy()
        file_specific_input["prefix"] = type_chars

        # 记录文件处理开始时间
        start_time = time.time()
        
        try:
            print(f"\nStarting Langda_Agent for {file_basename}...")
            # 用超时机制包装agent调用
            agent = Langda_Agent(rules_string, true_string, model_name, addition_input=file_specific_input)
            
            # 用超时机制包装call_langda_workflow调用
            print("Calling langda_workflow with timeout...")
            result = with_timeout(agent.call_langda_workflow, timeout)
            print(f"Workflow completed for {file_basename}")
            
        except Exception as e:
            print(f"Critical error in agent execution for {file_basename}: {str(e)}")
            traceback.print_exc()  # 打印完整的堆栈跟踪
            result = {
                "validity": "ERROR",
                "running_time": 0,
                "iter_count": 0,
                "final_result": f"Agent execution error: {str(e)}",
                "final_report": f"Stack trace: {traceback.format_exc()}"
            }
        
        # 计算处理耗时
        process_time = time.time() - start_time
        
        # Extract and format results
        try:
            validity = result.get("validity", "N/A")
            running_time = result.get("running_time", 0)
            iter_count = result.get("iter_count", 0)
            
            entry = {
                "type_chars": type_chars, 
                "validity": validity,
                "running_time": running_time,
                "iter_count": iter_count,
                "process_time": process_time,  # 添加处理耗时
                "final_result": result.get("final_result", ""),
                "final_report": result.get("final_report", "")
            }
            all_results.append(entry)
            
            # 也保存单独的JSON文件，方便查看单个结果
            json_output_path = os.path.join(os.path.dirname(output_json_path), f"{type_chars}_result.json")
            with open(json_output_path, 'w', encoding='utf-8') as json_file:
                json.dump(entry, json_file, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error processing results for {file_basename}: {str(e)}")
            entry = {
                "type_chars": type_chars,
                "error": str(e),
                "validity": "ERROR",
                "running_time": 0,
                "iter_count": 0,
                "process_time": process_time,
                "final_result": "",
                "final_report": ""
            }
            all_results.append(entry)
        
        # 更新进度条
        pbar.update(1)
        # 添加后处理信息到进度条
        pbar.set_postfix(validity=str(validity), time=f"{process_time:.1f}s")
        
        # 保存中间结果，防止长时间运行中断
        with open(output_json_path + ".temp", 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    # 关闭进度条
    pbar.close()
    
    # 计算总处理时间
    total_process_time = time.time() - total_start_time
    
    # 添加总结信息
    summary = {
        "total_files": total_files,
        "processed_files": len(all_results),
        "total_process_time": total_process_time,
        "average_process_time": total_process_time / len(all_results) if all_results else 0,
        "valid_count": sum(1 for r in all_results if str(r.get("validity")).lower() == "true"),
        "invalid_count": sum(1 for r in all_results if str(r.get("validity")).lower() == "false"),
        "error_count": sum(1 for r in all_results if r.get("validity") == "ERROR" or r.get("error"))
    }
    
    # 将结果和总结一起保存
    final_result = {
        "summary": summary,
        "results": all_results
    }
    
    # Save all results to a single JSON file
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessing Summary:")
    print(f"- Total files: {summary['total_files']}")
    print(f"- Processed: {summary['processed_files']}")
    print(f"- Valid: {summary['valid_count']}")
    print(f"- Invalid: {summary['invalid_count']}")
    print(f"- Errors: {summary['error_count']}")
    print(f"- Total time: {summary['total_process_time']:.1f}s")
    print(f"- Avg time per file: {summary['average_process_time']:.1f}s")
    
    return final_result

# 如果需要直接修改 problog_test_tool 函数，可以这样做：
def patched_problog_test_tool(model_string, timeout=60):
    """带有超时机制的 problog_test_tool 函数"""
    
    def _run_problog_test():
        print("Starting ProbLog evaluation...")
        try:
            from problog.program import PrologString
            from problog import get_evaluatable, evaluator
            
            print("Parsing ProbLog model...")
            evaluatable = get_evaluatable().create_from(PrologString(model_string))
            
            print("Evaluating model...")
            results = evaluatable.evaluate()
            
            print("Processing results...")
            result_lines = []
            for query_key, probability in results.items():
                result_line = f"{query_key} = {probability:.4f}"
                result_lines.append(result_line)
            
            return "% Problog Inference Result：\n" + "\n".join(result_lines)
        
        except Exception as e:
            error_msg = traceback.format_exc()
            print(f"Error in ProbLog evaluation: {str(e)}")
            print(error_msg)
            return f"Error evaluating Problog model:\n{error_msg}"
    
    return with_timeout(_run_problog_test, timeout)

if __name__ == "__main__":
    addition = {
        "usereact": True,
        "prefix": "",  # Will be updated for each file
        "langda_ext": "msg_from_bot",
        "error_report": "",
        "config": {"configurable": {"thread_id": "42"}},
        "user_context": ""
    }
    
    test_path = paths.get_abscase_path("rules/test_prompt")
    answer_path = paths.get_abscase_path("rules/test_answer")
    output_csv_path = paths.get_abscase_path("history/comparison_results.csv")
    output_json_path = paths.get_abscase_path("history/comparison_results.json")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    
    try:
        # 选项2: 使用JSON (更好地处理复杂内容)，设置超时为5分钟
        process_all_prompt_files_json(test_path, answer_path, "deepseek-chat", addition, output_json_path, timeout=300)
        print(f"JSON results saved to {output_json_path}")
    except Exception as e:
        print(f"Critical error in main execution: {str(e)}")
        traceback.print_exc()