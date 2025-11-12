"""Common utilities for data processing."""

import json
import re
from typing import Dict, Any, List


def load_task_info(task_info_path: str, task_name: str) -> Dict[str, Any]:
    """
    Load task information from jsonl file.

    Args:
        task_info_path: Path to the task info jsonl file
        task_name: Task name to look for

    Returns:
        Task information dictionary
    """
    with open(task_info_path, 'r', encoding='utf-8') as f:
        for line in f:
            task_data = json.loads(line.strip())
            if task_data.get('task_name') == task_name:
                return task_data
    raise ValueError(f"Task {task_name} not found in {task_info_path}")


def parse_task_actions(task_description: str) -> List[str]:
    """
    Parse action descriptions from task_description.

    Example:
        "action: Pick bread and place into wooden_box. Pick hammer and place into wooden_box. ..."
        Returns: ["Pick bread and place into wooden_box", "Pick hammer and place into wooden_box", ...]

    Args:
        task_description: Task description string containing actions

    Returns:
        List of action descriptions
    """
    # Extract the action part after "action: "
    # match = re.search(r'/action:\s*(.+)$', task_description)
    # if not match:
    #     raise ValueError(f"Cannot find action section in task_description: {task_description}")

    # action_text = match.group(1)
    # # Split by ". " but keep the periods
    # actions = []
    # for action in action_text.split('. '):
    #     action = action.strip()
    #     if action and not action.endswith('.'):
    #         action += '.'
    #     if action:
    #         actions.append(action.rstrip('.'))
    actions = task_description['action']
    return actions


def load_subplan(subplan_path: str) -> List[Dict[str, Any]]:
    """
    Load subplan from JSON file.

    Args:
        subplan_path: Path to subplan JSON file

    Returns:
        List of subplan entries
    """
    with open(subplan_path, 'r', encoding='utf-8') as f:
        return json.load(f)
