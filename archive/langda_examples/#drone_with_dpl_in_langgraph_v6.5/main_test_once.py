import os
import json
import time
import traceback
import statistics  # For calculating statistical data
from tqdm import tqdm
from config import paths
from agent import(
    LangdaAgentProtocol,
    LangdaAgentBase,
)
from agent import (
    LangdaAgentSingleSimple, 
    LangdaAgentDoubleSimple,
    LangdaAgentDoubleDC,
    LangdaAgentDCSimple,
    LangdaAgentSingleDC,
)
from collections import defaultdict

def process_all_prompt_files_json(test_directory_path, 
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
        with open(answer_file, "r") as f:
            true_string = f.read()

        # Read the rules from the prompt file
        with open(prompt_file, "r") as f:
            rules_string = f.read()
        
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
            
            print(f"\nStarting Langda_Agent for {file_basename} (Run {repeat_idx+1}/{repeat_count})...")

            agent:LangdaAgentProtocol = LangdaAgentDoubleDC(rules_string, true_string, model_name, addition_input=file_specific_input)
            print("Calling langda_workflow with timeout...")
            # Wrap call_langda_workflow with the with_timeout, prevent endless loop...
            result = agent.call_langda_workflow()

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

            # Calculate processing time for this run
            process_time = time.time() - start_time
            total_process_time += process_time
            file_process_times.append(process_time)
            
            # Extract and format result 
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

            # Update progress bar
            pbar.update(1)
            pbar.set_postfix(validity=str(result.get("Validity_result", "N/A")), time=f"{process_time:.1f}s", run=f"{repeat_idx+1}/{repeat_count}")

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
    print("It takes in total", overall_process_time, "seconds.")


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
    
    # Use JSON (better for complex content), set timeout to 5 minutes
    process_all_prompt_files_json(
        test_directory_path = test_path, 
        answer_directory_path = answer_path, 
        model_name = "deepseek-chat", 
        addition_input = addition, 
        output_json_dir = output_json_dir, 
        timeout=300,
        repeat_count=repeat_count  
    )
    print(f"JSON results saved to {output_json_dir}")
