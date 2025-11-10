"""
Batch process tasks from jsonl file, call model to generate execution code (only generate code, no detection)

Usage:
python code_gen/batch_generate_from_jsonl.py <jsonl_file_path> [options]

Example:
python code_gen/batch_generate_from_jsonl.py code_gen/task_info/common_sense_correction.jsonl --all
python code_gen/batch_generate_from_jsonl.py code_gen/task_info/common_sense_correction.jsonl --start 0 --end 10
python code_gen/batch_generate_from_jsonl.py code_gen/task_info/common_sense_correction.jsonl --task_names task1 task2
"""

import sys
import os
import json
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Add the project root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code_gen.gpt_agent import generate
from code_gen.new_prompt import (
    BASIC_INFO,
    AVAILABLE_ENV_FUNCTION_LOAD_ACTORS,
    AVAILABLE_ENV_FUNCTION_PLAY_ONCE,
    AVAILABLE_ENV_FUNCTION_CHECK_SUCCESS,
    FUNCTION_EXAMPLE
)


def fix_indentation(code):
    """Fix code indentation"""
    lines = code.split('\n')
    if code.find('\tdef') == -1 and code.find("    def") == -1:
        print("Need to add indentation!")
        fixed_lines = ['\t' + line for line in lines]
        return '\n'.join(fixed_lines)
    else:
        return code


def generate_code_for_task(task_info, gpt_model="local", temperature=0):
    """
    Generate code for a single task (generate only, no detection)

    Args:
        task_info: Task information dict containing task_name and task_description
        gpt_model: Model type to use
        temperature: Generation temperature

    Returns:
        Generated code string
    """
    # Extract task information
    task_name = task_info['task_name']
    task_description = task_info['task_description']

    print(f"Generating code for task: {task_name}")
    print(f"Task description: {task_description[:100]}...")

    # Get API information
    available_env_function_load_actors = str(AVAILABLE_ENV_FUNCTION_LOAD_ACTORS)
    available_env_function_play_once = str(AVAILABLE_ENV_FUNCTION_PLAY_ONCE)
    available_env_function_check_success = str(AVAILABLE_ENV_FUNCTION_CHECK_SUCCESS)
    function_example = str(FUNCTION_EXAMPLE)

    # Build complete prompt
    Prompt = (
        f"{BASIC_INFO}\n\n"
        f"# Task Description: \n{task_description}\n\n"
        f"# Available API for loading actors: \n{available_env_function_load_actors}\n\n"
        f"# Available API for play_once: \n{available_env_function_play_once}\n\n"
        f"# Available API for checking success: \n{available_env_function_check_success}\n\n"
        f"# Function Example: \n{function_example}\n\n"
    )

    # Build messages
    messages = [
        {"role": "system", "content": "You need to generate relevant code for robot tasks in a robot simulation environment based on the provided APIs."},
        {"role": "user", "content": Prompt}
    ]

    def gpt_agent(messages: List[Dict[str, str]], temperature: float = 0.0) -> str:
        from zai import ZhipuAiClient
        API_KEY = os.environ.get("OPENAI_API_KEY", "a540dedc345f7f25a6e5443cf533cc11.P1UxjgNxul3PEP0d")
        MODEL = "glm-4-flash"

        # client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
        client = ZhipuAiClient(api_key=API_KEY)
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            # stream=False,
            temperature=temperature,
        )
        return resp.choices[0].message.content

    # Use model to generate code
    print("Calling model to generate...")
    # res = generate(messages, gpt=gpt_model, temperature=temperature)
    res = gpt_agent(messages, temperature=temperature)
    print("Model generation completed")

    # Extract relevant parts of the generated code
    res = fix_indentation(res)
    load_actors_start = res.find("def load_actors(self):")
    play_once_start = res.find("def play_once(self):")
    check_success_start = res.find("def check_success(self):")
    check_success_end = res.find("```\n")

    # If end marker not found, use end of string
    if check_success_end == -1:
        check_success_end = len(res)

    # Extract code for each method
    load_actors_code = res[load_actors_start:play_once_start].strip() if play_once_start > load_actors_start else ""
    play_once_code = res[play_once_start:check_success_start].strip() if check_success_start > play_once_start else ""
    check_success_code = res[check_success_start:check_success_end].strip()

    # Generate final code, class name directly uses task_name
    final_code = f'''from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class {task_name}(Imagine_Task):
    {load_actors_code}

    {play_once_code}

    {check_success_code}
'''

    return final_code


def load_tasks_from_jsonl(jsonl_file_path):
    """Load all tasks from jsonl file"""
    tasks = []
    with open(jsonl_file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    task = json.loads(line)
                    tasks.append(task)
                except json.JSONDecodeError as e:
                    print(f"Warning: Line {line_num} JSON parsing failed: {e}")
                    continue
    return tasks


def process_tasks_batch(jsonl_file_path, output_dir="envs_gen", start_idx=0,
                        end_idx=None, task_names=None, gpt_model="local", temperature=0):
    """
    Batch process tasks from jsonl file and generate code

    Args:
        jsonl_file_path: jsonl file path
        output_dir: output directory
        start_idx: start task index
        end_idx: end task index (exclusive)
        task_names: list of task names to process
        gpt_model: model type to use (deepseek, openai, local)
        temperature: generation temperature
    """

    # Check if file exists
    if not os.path.exists(jsonl_file_path):
        print(f"Error: File {jsonl_file_path} does not exist")
        return

    # Extract jsonl file basename (without extension) to create subdirectory
    jsonl_basename = os.path.basename(jsonl_file_path).replace('.jsonl', '')

    # Create output directory with subdirectory based on jsonl filename
    task_output_dir = os.path.join(output_dir, jsonl_basename)
    os.makedirs(task_output_dir, exist_ok=True)

    # Load all tasks
    all_tasks = load_tasks_from_jsonl(jsonl_file_path)
    print(f"Loaded {len(all_tasks)} tasks from {jsonl_file_path}\n")
    print(f"Output directory: {task_output_dir}\n")

    # Filter tasks based on parameters
    if task_names:
        # Filter by task names
        tasks_to_process = [t for t in all_tasks if t['task_name'] in task_names]
        print(f"Filtered by task names, will process {len(tasks_to_process)} tasks")
    else:
        # Filter by index range
        end_idx = end_idx if end_idx is not None else len(all_tasks)
        tasks_to_process = all_tasks[start_idx:end_idx]
        print(f"Will process tasks from index {start_idx} to {end_idx-1}, total {len(tasks_to_process)} tasks\n")

    if len(tasks_to_process) == 0:
        print("No tasks to process")
        return

    # Create summary report list
    summary_results = []

    # Process each task
    for idx, task in enumerate(tasks_to_process):
        print(f"\n{'='*80}")
        print(f"Processing task {idx+1}/{len(tasks_to_process)}: {task['task_name']}")
        print(f"{'='*80}\n")

        try:
            # Generate code
            generated_code = generate_code_for_task(task, gpt_model=gpt_model, temperature=temperature)

            # Save generated code to subdirectory
            output_file = os.path.join(task_output_dir, f"{task['task_name']}.py")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(generated_code)

            print(f"✓ Code saved to: {output_file}")

            result = {
                "task_name": task['task_name'],
                "task_description": task['task_description'],
                "output_file": output_file,
                "status": "success"
            }
            summary_results.append(result)

        except KeyboardInterrupt:
            print(f"\n\nUser interrupted processing")
            print(f"Processed {idx} tasks, {len(tasks_to_process) - idx} tasks remaining")
            break
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"✗ Error occurred while processing task {task['task_name']}: {e}")
            print(f"Error details:\n{error_trace}")

            result = {
                "task_name": task['task_name'],
                "task_description": task['task_description'],
                "output_file": None,
                "status": "error",
                "error": str(e)
            }
            summary_results.append(result)

    # Save summary report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = os.path.join(output_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    summary_filename = os.path.join(log_dir, f"batch_summary_{jsonl_basename}_{timestamp}.json")

    successful_tasks = sum(1 for r in summary_results if r['status'] == 'success')
    error_tasks = sum(1 for r in summary_results if r['status'] == 'error')

    with open(summary_filename, 'w', encoding='utf-8') as f:
        summary_data = {
            "jsonl_file": jsonl_file_path,
            "output_dir": task_output_dir,
            "total_tasks": len(tasks_to_process),
            "successful_tasks": successful_tasks,
            "error_tasks": error_tasks,
            "model": gpt_model,
            "temperature": temperature,
            "results": summary_results,
            "timestamp": timestamp
        }
        json.dump(summary_data, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*80}")
    print(f"Batch processing completed!")
    print(f"{'='*80}")
    print(f"Total processed: {len(tasks_to_process)} tasks")
    print(f"Successful: {successful_tasks} tasks")
    print(f"Errors: {error_tasks} tasks")
    print(f"\nCode saved to directory: {task_output_dir}")
    print(f"Summary report saved to: {summary_filename}")
    print(f"{'='*80}\n")

    # Print detailed results
    print("\nDetailed results:")
    for i, result in enumerate(summary_results, 1):
        status_symbol = "✓" if result['status'] == 'success' else "✗"
        print(f"{i}. {status_symbol} {result['task_name']} -> {result.get('output_file', 'N/A')}")

    return summary_results


def main():
    parser = argparse.ArgumentParser(
        description='Batch process tasks from jsonl file and generate execution code (generate only, no detection)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  # Process all tasks
  python code_gen/batch_generate_from_jsonl.py code_gen/task_info/common_sense_correction.jsonl --all

  # Process first 10 tasks
  python code_gen/batch_generate_from_jsonl.py code_gen/task_info/common_sense_correction.jsonl --start 0 --end 10

  # Process specified tasks
  python code_gen/batch_generate_from_jsonl.py code_gen/task_info/common_sense_correction.jsonl --task_names task1 task2

  # Use different model and output directory
  python code_gen/batch_generate_from_jsonl.py code_gen/task_info/common_sense_correction.jsonl --all --model deepseek --output envs_generated
        """
    )

    parser.add_argument(
        'jsonl_file',
        type=str,
        help='Input jsonl file path'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Process all tasks'
    )

    parser.add_argument(
        '--start',
        type=int,
        default=0,
        help='Start task index (default: 0)'
    )

    parser.add_argument(
        '--end',
        type=int,
        default=None,
        help='End task index (default: process to the end)'
    )

    parser.add_argument(
        '--task_names',
        nargs='+',
        default=None,
        help='List of task names to process'
    )

    parser.add_argument(
        '--model',
        type=str,
        default='local',
        choices=['deepseek', 'openai', 'local'],
        help='Model type to use (default: local)'
    )

    parser.add_argument(
        '--temperature',
        type=float,
        default=0,
        help='Generation temperature (default: 0)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='envs_gen',
        help='Output directory (default: envs_gen)'
    )

    args = parser.parse_args()

    # If --all is specified, ignore start and end
    if args.all:
        args.start = 0
        args.end = None
        print("Processing mode: All tasks\n")

    # Execute batch processing
    process_tasks_batch(
        jsonl_file_path=args.jsonl_file,
        output_dir=args.output,
        start_idx=args.start,
        end_idx=args.end,
        task_names=args.task_names,
        gpt_model=args.model,
        temperature=args.temperature
    )


if __name__ == "__main__":
    main()
