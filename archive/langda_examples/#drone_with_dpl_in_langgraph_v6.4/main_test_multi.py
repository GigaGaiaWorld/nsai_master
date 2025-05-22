import os
import json
import time
import traceback
import statistics  # For calculating statistical data
from tqdm import tqdm
from config import paths
from utils import with_timeout
from agent import(
    LangdaAgentProtocol,
    LangdaAgentBase,
)
from collections import defaultdict
def process_all_prompt_files_json(Agent:LangdaAgentBase, 
                                  test_directory_path, 
                                  answer_directory_path, 
                                  model_name, 
                                  addition_input, 
                                  output_json_dir, 
                                  timeout=300, repeat_count=1):
    
    # Track summary statistics without storing all results in memory
    file_summaries = []
    success_form_count = 0
    success_result_count = 0
    invalid_form_count = 0
    invalid_result_count = 0
    error_count = 0
    total_process_time = 0
    total_runs = 0
    
    final_result_path = os.path.join(output_json_dir, "_final_result.json")
    
    # Find all prompt files
    prompt_files = []
    for root, _, files in os.walk(test_directory_path):
        for file in files:
            prompt_files.append(os.path.join(root, file))

    total_files = len(prompt_files)
    print(f"*** Found {total_files} files to process ***")
    print(f"*** Each file will be processed {repeat_count} times ***")
    total_iterations = total_files * repeat_count
    pbar = tqdm(total=total_iterations, desc="Processing files")
    overall_start_time = time.time()
    
    # Process each prompt file
    for idx, prompt_file in enumerate(prompt_files, start=1):
        file_basename = os.path.basename(prompt_file)
        file_results = []  # Store results for this file only
        
        # Find corresponding answer file
        answer_file = None
        for root, _, files in os.walk(answer_directory_path):
            for file in files:
                if file.startswith(file_basename[:10]):
                    answer_file = os.path.join(root, file)
                    break
            if answer_file:
                break

        if not answer_file:
            print(f"Warning: No matching answer file found for answer_file: {file_basename[:10]}, skipping")
            pbar.update(repeat_count)  # Update progress bar, skip all repeats
            continue

        # Read answer file for comparison (true_string)
        try:
            with open(answer_file, "r") as f:
                true_string = f.read()
        except Exception as e:
            print(f"Error reading answer file {answer_file}: {str(e)}")
            pbar.update(repeat_count)  # Update progress bar, skip all repeats
            continue

        # Read the rules from the prompt file
        try:
            with open(prompt_file, "r") as f:
                rules_string = f.read()
        except Exception as e:
            print(f"Error reading prompt file {prompt_file}: {str(e)}")
            pbar.update(repeat_count)  # Update progress bar, skip all repeats
            continue
        
        # Local counters for this file
        file_success_form_count = 0
        file_success_result_count = 0
        file_invalid_form_count = 0
        file_invalid_result_count = 0
        file_error_count = 0
        file_process_times = []
        
        # Repeat execution n times
        for repeat_idx in range(repeat_count):
            total_runs += 1
            process_time = 0
            repeat_suffix = f"[{repeat_idx+1}/{repeat_count}]" if repeat_count > 1 else ""
            pbar.set_description(f"*** Processing {file_basename} [{idx}/{total_files}] {repeat_suffix} ***")
            file_name = f"{file_basename}_run{repeat_idx+1}"

            # Update the prefix in addition_input
            file_specific_input = addition_input.copy()
            file_specific_input["prefix"] = file_name
            
            # File process start time
            start_time = time.time()
            try:
                print(f"\nStarting Langda_Agent for {file_basename} (Run {repeat_idx+1}/{repeat_count})...")

                agent:LangdaAgentProtocol = Agent(rules_string, true_string, model_name, addition_input=file_specific_input)
                print("Calling langda_workflow with timeout...")
                # Wrap call_langda_workflow with the with_timeout, prevent endless loop...
                result = with_timeout(agent.call_langda_workflow, file_name, timeout)

                if isinstance(result, str) and result.startswith("ERROR: Execution timed out"):
                    print(f"Timeout occurred for {file_basename} (Run {repeat_idx+1})")
                    result = {
                        "file_name": file_basename, 
                        "Validity_form": "TIMEOUT",
                        "Validity_result": "TIMEOUT",
                        "running_time": f">= {timeout}",
                        "iter_count": 0,
                        "process_time": process_time,
                        "final_result": "TIMEOUT",
                        "final_report": "Function execution timed out",
                        "run_index": repeat_idx+1
                    }
                    file_error_count += 1
                    error_count += 1
                else:
                    print(f"Workflow completed for {file_basename} (Run {repeat_idx+1})")
                    # Ensure result includes run index
                    result["run_index"] = repeat_idx+1
                    
                    # Count successes and failures
                    if str(result.get("Validity_form", "")).lower() == "true":
                        file_success_form_count += 1
                        success_form_count += 1
                    elif str(result.get("Validity_form", "")).lower() == "false":
                        file_invalid_form_count += 1
                        invalid_form_count += 1
                    else:
                        file_error_count += 1
                        error_count += 1
                         
                    if str(result.get("Validity_result", "")).lower() == "true":
                        file_success_result_count += 1
                        success_result_count += 1
                    elif str(result.get("Validity_result", "")).lower() == "false":
                        file_invalid_result_count += 1
                        invalid_result_count += 1

            except Exception as e:
                print(f"Critical error in agent execution for {file_basename} (Run {repeat_idx+1}): {str(e)}")
                traceback.print_exc()
                result = {
                    "file_name": file_basename, 
                    "Validity_form": "ERROR",
                    "Validity_result": "ERROR",
                    "running_time": "None",
                    "iter_count": "None",
                    "process_time": process_time,
                    "final_result": f"Agent execution error: {str(e)}",
                    "final_report": f"Stack trace: {traceback.format_exc()}",
                    "run_index": repeat_idx+1
                }
                file_error_count += 1
                error_count += 1

            # Calculate processing time for this run
            process_time = time.time() - start_time
            total_process_time += process_time
            file_process_times.append(process_time)
            
            # Extract and format result 
            try:
                entry = {
                    "file_name": file_basename, 
                    "run_index": repeat_idx+1,  # Add run index
                    "Validity_form": result.get("Validity_form", "N/A"),
                    "Validity_result": result.get("Validity_result", "N/A"),
                    "running_time": result.get("running_time", "None"),
                    "iter_count": result.get("iter_count", "None"),
                    "process_time": process_time
                }
                
                # Add to file results list
                file_results.append(entry)

                # Save individual run result to a separate JSON file
                json_output_path = os.path.join(output_json_dir, f"{file_basename}_run{repeat_idx+1}_result.json")
                with open(json_output_path, 'w', encoding='utf-8') as json_file:
                    # Save the full result including final_result/final_report to the individual file
                    full_entry = entry.copy()
                    full_entry["final_result"] = result.get("final_result", "")
                    full_entry["final_report"] = result.get("final_report", "")
                    json.dump(full_entry, json_file, indent=2, ensure_ascii=False)

            except Exception as e:
                print(f"Error processing results for {file_basename} (Run {repeat_idx+1}): {str(e)}")
                
                # Update counters even on error
                file_error_count += 1
                error_count += 1

            # Update progress bar
            pbar.update(1)
            pbar.set_postfix(validity=str(result.get("Validity_result", "N/A")), time=f"{process_time:.1f}s", run=f"{repeat_idx+1}/{repeat_count}")

            break
        # Calculate and save summary statistics for this file
        if file_process_times:
            file_summary = {
                "file_name": file_basename,
                "runs": repeat_count,
                "avg_process_time": statistics.mean(file_process_times),
                "min_process_time": min(file_process_times),
                "max_process_time": max(file_process_times),
                "std_dev_time": statistics.stdev(file_process_times) if len(file_process_times) > 1 else 0,
                "success_form_count": file_success_form_count,
                "success_result_count": file_success_result_count,
                "invalid_form_count": file_invalid_form_count,
                "invalid_result_count": file_invalid_result_count,
                "error_count": file_error_count,
                "success_form_rate": file_success_form_count / repeat_count if repeat_count > 0 else 0,
                "success_result_rate": file_success_result_count / repeat_count if repeat_count > 0 else 0
            }
            
            # Add to global file summaries list (without individual results)
            file_summaries.append(file_summary)
            
            # Save file summary to separate JSON
            summary_output_path = os.path.join(output_json_dir, f"{file_basename}_summary.json")
            with open(summary_output_path, 'w', encoding='utf-8') as json_file:
                # Include individual results only in the per-file summary
                summary_with_details = file_summary.copy()
                summary_with_details["individual_results"] = file_results
                json.dump(summary_with_details, json_file, indent=2, ensure_ascii=False)
                
            print(f"\nSummary for {file_basename}:")
            print(f"- Success form rate: {file_summary['success_form_rate']*100:.1f}%")
            print(f"- Success result rate: {file_summary['success_result_rate']*100:.1f}%")
            print(f"- Avg process time: {file_summary['avg_process_time']:.1f}s")
            
        # Save intermediate results without storing all individual run details
        with open(final_result_path + ".temp", 'w', encoding='utf-8') as f:
            intermediate_summary = {
                "files_processed": idx,
                "total_files": total_files,
                "repeat_count": repeat_count,
                "total_runs_completed": total_runs,
                "success_form_count": success_form_count,
                "success_result_count": success_result_count,
                "invalid_form_count": invalid_form_count,
                "invalid_result_count": invalid_result_count,
                "error_count": error_count,
                "file_summaries": file_summaries
            }
            json.dump(intermediate_summary, f, indent=2, ensure_ascii=False)
    
    pbar.close()
    # =============== Total Summary =============== #
    overall_process_time = time.time() - overall_start_time
    print("It takes in total",overall_process_time,"seconds.")


def generate_final_report_from_json(json_directory, output_final_path=None):
    """
    Generate a final statistical report from JSON result files in specified directory
    
    Args:
        json_directory: Path to directory containing result JSON files
        output_final_path: Path to save final report (defaults to _final_result.json in json_directory)
    
    Returns:
        Dictionary containing the final summary report
    """
    
    # Initialize counters
    total_files = 0
    total_runs = 0
    success_form_count = 0
    success_result_count = 0
    invalid_form_count = 0
    invalid_result_count = 0
    error_count = 0
    total_process_time = 0
    
    # Group all runs by file name
    file_results = defaultdict(list)
    file_summaries = []
    
    # Find all result files
    result_files = [os.path.join(json_directory, f) for f in os.listdir(json_directory) 
                    if f.endswith("_result.json") and not f.startswith("_final")]
    
    # Process all result files
    for result_file in result_files:
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                
            file_name = result.get("file_name")
            if file_name:
                file_results[file_name].append(result)
                total_runs += 1
                
                # Count validity forms
                validity_form = str(result.get("Validity_form", "")).lower()
                validity_result = str(result.get("Validity_result", "")).lower()
                
                if validity_form == "true":
                    success_form_count += 1
                elif validity_form == "false":
                    invalid_form_count += 1
                elif validity_form in ["error", "timeout"]:
                    error_count += 1
                    
                if validity_result == "true":
                    success_result_count += 1
                elif validity_result == "false":
                    invalid_result_count += 1
                
                # Sum process time
                process_time = result.get("process_time", 0)
                if isinstance(process_time, (int, float)):
                    total_process_time += process_time
                
        except Exception as e:
            print(f"Error processing file {result_file}: {str(e)}")
    
    # Calculate statistics for each file
    unique_files = set(file_results.keys())
    total_files = len(unique_files)
    
    for file_name, results in file_results.items():
        repeat_count = len(results)
        
        # Calculate file-specific statistics
        file_success_form_count = sum(1 for r in results if str(r.get("Validity_form", "")).lower() == "true")
        file_success_result_count = sum(1 for r in results if str(r.get("Validity_result", "")).lower() == "true")
        file_invalid_form_count = sum(1 for r in results if str(r.get("Validity_form", "")).lower() == "false")
        file_invalid_result_count = sum(1 for r in results if str(r.get("Validity_result", "")).lower() == "false")
        file_error_count = sum(1 for r in results if str(r.get("Validity_form", "")).lower() in ["error", "timeout"])
        
        # Calculate time statistics
        file_process_times = [r.get("process_time", 0) for r in results 
                             if isinstance(r.get("process_time", 0), (int, float))]
        
        if file_process_times:
            file_summary = {
                "file_name": file_name,
                "runs": repeat_count,
                "avg_process_time": statistics.mean(file_process_times),
                "min_process_time": min(file_process_times),
                "max_process_time": max(file_process_times),
                "std_dev_time": statistics.stdev(file_process_times) if len(file_process_times) > 1 else 0,
                "success_form_count": file_success_form_count,
                "success_result_count": file_success_result_count,
                "invalid_form_count": file_invalid_form_count,
                "invalid_result_count": file_invalid_result_count,
                "error_count": file_error_count,
                "success_form_rate": file_success_form_count / repeat_count if repeat_count > 0 else 0,
                "success_result_rate": file_success_result_count / repeat_count if repeat_count > 0 else 0
            }
            
            file_summaries.append(file_summary)

    # Set output path
    if output_final_path is None:
        output_final_path = os.path.join(json_directory, "_final_result.json")
    
    # Calculate overall summary
    summary = {
        "total_files": total_files, "repeat_count": repeat_count, "total_runs": total_runs,
        "total_process_time": total_process_time,
        "average_process_time": total_process_time / total_runs if total_runs else 0,
        "success_form_count": success_form_count, "success_result_count": success_result_count,
        "invalid_form_count": invalid_form_count, "invalid_result_count": invalid_result_count,
        "error_count": error_count,
        "overall_success_form_rate": success_form_count / total_runs if total_runs else 0,
        "overall_success_result_rate": success_result_count / total_runs if total_runs else 0,
    }
    
    # Add file success rates
    if repeat_count > 1:
        file_rates = {
            s["file_name"]: {
                "success_form_rate": s["success_form_rate"],
                "success_result_rate": s["success_result_rate"]
            }
            for s in file_summaries
        }
        summary["file_success_rates"] = file_rates
    
    # Create final result
    final_result = {
        "summary": summary,
        "file_summaries": file_summaries
    }
    
    # Save final result
    with open(output_final_path, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, indent=2, ensure_ascii=False)
    
    if repeat_count > 1:
        print(f"- Overall success form rate: {summary['overall_success_form_rate']*100:.1f}%")
        print(f"- Overall success result rate: {summary['overall_success_result_rate']*100:.1f}%")
    
    return final_result

from agent import (
    LangdaAgentSingleSimple, 
    LangdaAgentDoubleSimple,
    LangdaAgentDoubleDC,
    LangdaAgentDCSimple,
    LangdaAgentSingleDC,
)

if __name__ == "__main__":
    addition = {
        "prefix": "",  # Will be updated for each file
        "langda_ext": "msg_from_bot",
        "error_report": "",
        "config": {"configurable": {"thread_id": "42"}},
        "user_context": ""
    }

    test_path = paths.get_abscase_path("rules/test_prompt")
    answer_path = paths.get_abscase_path("rules/test_answer")
    output_json_dir = paths.get_abscase_path("history/json")
    output_json_dir.mkdir(parents=True, exist_ok=True)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_json_dir), exist_ok=True)
    
    # Set repeat count
    repeat_count = 5  # Default 5 times, can be adjusted as needed
    
    try:
        #                     *** MAIN FUNCTION ***                     #
        # Use JSON (better for complex content), set timeout to 5 minutes
        process_all_prompt_files_json(
            Agent = LangdaAgentDoubleDC,  
            test_directory_path = test_path, 
            answer_directory_path = answer_path, 
            model_name = "deepseek-chat", 
            addition_input = addition, 
            output_json_dir = output_json_dir, 
            timeout=300,
            repeat_count=repeat_count  
        )
        print(f"JSON results saved to {output_json_dir}")
        generate_final_report_from_json(output_json_dir, os.path.join(output_json_dir,"_final_result.json"))
    except Exception as e:
        print(f"Critical error in main execution: {str(e)}")
        traceback.print_exc()