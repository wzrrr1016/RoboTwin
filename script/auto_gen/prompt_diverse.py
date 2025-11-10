from typing import List, Dict, Optional, Any
import json
import random
import os
import sys
try:
    from .all_object import ATTR_KB, CONTAINER_KB, DISTRACTOR_KB
except Exception:
    # When executed as a script: python script/auto_gen/generate_task_info_diverse.py
    _CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    if _CURR_DIR not in sys.path:
        sys.path.append(_CURR_DIR)
    from all_object import ATTR_KB, CONTAINER_KB, DISTRACTOR_KB

def _format_selected(containers: List[str], object_candidates: List[str]) -> str:
    return (
        "Candidate containers: " + ", ".join(containers) + "\n" +
        "Candidate task objects pool (choose 3-5 from these): " + ", ".join(object_candidates)
    )


# Color theory (RGB additive color model - mixing outcomes)
COLOR_MIX = {
    "red+green": "yellow",      # primary + primary = secondary
    "red+blue": "purple",        # primary + primary = secondary (magenta)
    "red+yellow": "orange",      # primary + secondary = tertiary
}


def _format_attribute_sheet(containers: List[str], object_candidates: List[str]) -> str:
    lines: List[str] = []
    lines.append("Attributes (use for reasoning, do not invent):")
    for c in containers:
        lines.append(f"- {c}: " + ", ".join(CONTAINER_KB.get(c, ["container"])))
    for obj in object_candidates:
        tags = ATTR_KB.get(obj, [])
        if tags:
            lines.append(f"- {obj}: " + ", ".join(tags))
    lines.append("Color mixing: " + ", ".join(f"{k}=>{v}" for k, v in COLOR_MIX.items()))
    return "\n".join(lines)


def _recent_summaries(previous_descs: List[str], max_items: int = 12) -> str:
    if not previous_descs:
        return "(none)"
    prev = previous_descs[-max_items:]
    newline_char = '\n'
    return "\n".join(f"{i}. {p.replace(newline_char, ' ')[:220]}" for i, p in enumerate(prev, 1))


def _examples_correction() -> str:
    ex1 = {
        "task_name": "healthy_food_placement_correction",
        "task_description": {
            "scene": {
                "containers": ["plate", "wooden_box"],
                "objects": ["apple", "hamburg", "french_fries","bread"]
            },
            "task": "Put the healthy items into the plate and unhealthy items into the wooden_box.",
            "action": [
                "Pick apple and place it into wooden_box (wrong)",
                "Pick apple from wooden_box and place it into plate (recovery)",
                "Pick bread and place it into plate",
                "Pick hamburg and place it into wooden_box",
                "Pick french_fries and place it into wooden_box"
            ]
        }
    }
    ex2 = {
        "task_name": "liquid_container_grouping_correction",
        "task_description": {
            "scene": {
                "containers": ["coaster", "dustbin"],
                "objects": ["bottle", "cup_with_handle", "mug", "cup_without_handle"]
            },
            "task": "Put drinkware with handles into the coaster and those without handles into the dustbin.",
            "action": [
                "Pick bottle and place it into coaster (wrong)",
                "Pick bottle from coaster and place it into dustbin (recovery)",
                "Pick cup_without_handle and place it into dustbin",
                "Pick cup_with_handle and place it into coaster",
                "Pick mug and place it into coaster"
            ]
        }
    }
    return json.dumps(ex1, ensure_ascii=False) + "\n" + json.dumps(ex2, ensure_ascii=False)


def _examples_wo_correction() -> str:
    ex1 = {
        "task_name": "shoe_storage_task",
        "task_description": {
            "scene": {
                "containers": ["shoe_box", "wooden_box"],
                "objects": ["shoe", "screwdriver", "drill"]
            },
            "task": "Put footwear items into their designated storage and repair tools into general storage.",
            "action": [
                "Pick shoe and place it into shoe_box",
                "Pick screwdriver and place it into wooden_box",
                "Pick drill and place into it wooden_box"
            ]
        }
    }
    ex2 = {
        "task_name": "time_utility_organization",
        "task_description": {
            "scene": {
                "containers": ["tray", "dustbin"],
                "objects": ["alarm-clock", "sand-clock", "bell"]
            },
            "task": "Put time-related items into the tray and sound-only items into the dustbin.",
            "action": [
                "Pick alarm-clock and place it into tray",
                "Pick sand-clock and place it into tray",
                "Pick bell and place into it dustbin"
            ]
        }
    }
    return json.dumps(ex1, ensure_ascii=False) + "\n" + json.dumps(ex2, ensure_ascii=False)


def _system_block(mode: str) -> str:
    if mode == "correction":
        return (
            "Design a pick-place task with common sense reasoning and ONE mistake that gets corrected.\n"
            "Output JSON format: {'task_name': '...', 'task_description': {'scene': {'containers': [...], 'objects': [...]}, 'task': '...', 'action': [...]}}\n\n"
            "Process:\n"
            "1. Select 1-2 containers from the provided list\n"
            "2. Select 3-5 objects from the 'task objects pool'\n"
            "3. Design the task based on common-sense properties\n"
            "4. Design actions with ONE mistake\n\n"
            "Requirements:\n"
            "- Use ONLY provided containers and objects\n"
            "- scene: JSON format with 'containers' (list) and 'objects' (list)\n"
            "- task: Single string describing the task using common-sense categories or features.Don't use one feature for one item, but a feature for a few objects. (e.g., 'Put healthy foods into plate')\n"
            "  * NO specific item names, NO vague phrases like 'sort by color'\n" 
            "  * Don't use opposite categories that every objects in the world can be categoried into the two categories(e.g., electronic item and non-electronic item)\n"
            "- action: List of strings, each 'Pick X and place it into/on Y'\n"
            "  * Include ONE mistake: mark with '(wrong)', then correct with '(recovery)'. \n"
            "  * Mistake can occur at any step\n"
            "  Mistake can be pick a wrong object and put it back on the table, or put an object into/on a wrong container and then correct it.\n"
            "  * MAXIMUM 6 operations (including correction)\n"
        )
    else:
        return (
            "Design a pick-place task with common sense reasoning.\n"
            "Output JSON format: {'task_name': '...', 'task_description': {'scene': {'containers': [...], 'objects': [...]}, 'task': '...', 'action': [...]}}\n\n"
            "Process:\n"
            "1. Select 1-2 containers from the provided list\n"
            "2. Select 3-5 objects from the 'task objects pool' that share common attributes for your task\n"
            "3. Design the task based on common-sense properties\n"
            "4. Design correct actions\n\n"
            "Requirements:\n"
            "- Use ONLY provided containers and objects\n"
            "- scene: JSON format with 'containers' (list) and 'objects' (list)\n"
            "- task: Single string describing the task using common-sense categories (e.g., 'Put healthy foods into plate')\n"
            "  * NO specific item names, NO vague phrases like 'arrange by color'\n"
            "  * Don't use opposite categories (e.g., 'electronic vs non-electronic')\n"
            "- action: List of strings, each 'Pick X and place it into/on Y'\n"
            "  * All actions correct, NO mistakes\n"
            "  * MAXIMUM 6 operations\n"
        )


def common_sense_diverse(previous_descs: List[str], selected_containers: List[str],
                        object_candidates: List[str], mode: str) -> List[Dict[str, str]]:
    system = _system_block(mode)
    recent = _recent_summaries(previous_descs)
    attr_sheet = _format_attribute_sheet(selected_containers, object_candidates)

    user = (
        _format_selected(selected_containers, object_candidates) + "\n\n" +
        attr_sheet + "\n\n" +
        # "Recent tasks (avoid similar):\n" + recent + "\n\n" +
        "Design ONE new task using ONLY candidates above.\n"
        "Return one JSON object.\n\n"
        "Examples:\n" +
        (_examples_correction() if mode == "correction" else _examples_wo_correction())
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def common_sense_correction(previous_descs: List[str], selected_containers: List[str],
                           object_candidates: List[str]) -> List[Dict[str, str]]:
    return common_sense_diverse(previous_descs, selected_containers, object_candidates, mode="correction")


def common_sense_wo_correction(previous_descs: List[str], selected_containers: List[str],
                               object_candidates: List[str]) -> List[Dict[str, str]]:
    return common_sense_diverse(previous_descs, selected_containers, object_candidates, mode="wo_correction")


# New function for distractor selection (Stage 2)
def select_distractors_prompt(task_description: Dict[str, Any], distractor_candidates: List[str],
                              previous_distractors: Optional[List[str]] = None,
                              validation_error: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Generate prompt for LLM to select distractors that are irrelevant to the task.

    Args:
        task_description: Task description dict
        distractor_candidates: Available distractor candidates (not used if using all from DISTRACTOR_KB)
        previous_distractors: Previously selected distractors that failed validation (optional)
        validation_error: The validation error message (optional)
    """
    task_text = task_description.get("task", "")
    objects = task_description.get("scene", {}).get("objects", [])

    # Get all available distractors (excluding task objects)
    distractor_info = DISTRACTOR_KB.keys()
    distractor_info = [k for k in distractor_info if k not in objects]

    system = (
        "You are selecting distractor objects for a robotic pick-and-place task.\n"
        "Distractors are objects that should be present in the scene but NOT manipulated or mentioned in the task.\n"
        "They must be completely IRRELEVANT to the task objectives."
    )

    user_parts = []
    user_parts.append(f"Task description: {task_text}\n")
    user_parts.append(f"Task objects (objects being manipulated): {', '.join(objects)}\n")

    # If this is a retry, show previous failure
    if previous_distractors and validation_error:
        user_parts.append(f"\n⚠️ PREVIOUS ATTEMPT FAILED ⚠️")
        user_parts.append(f"Previously selected distractors: {', '.join(previous_distractors)}")
        user_parts.append(f"Validation error: {validation_error}")
        user_parts.append(f"Please select DIFFERENT distractors that avoid this error.\n")

    user_parts.append(f"Available distractor candidates:\n" + "\n".join(distractor_info) + "\n")
    user_parts.append(
        "Select 3-6 distractors that are:\n"
        "1. Completely UNRELATED to the task objectives\n"
        "2. NOT in the same category as task objects\n"
        "3. Would NOT be confused with task objects\n"
        "4. Do NOT share attributes mentioned in the task description\n\n"
        "CRITICAL: DON'T select items that could be categorized by the same properties mentioned in the task.\n"
        "Example: If task is 'Put drinkware items...', don't select items that are drinkware.\n\n"
        "Return JSON format: {\"distractors\": [\"item1\", \"item2\", ...]}\n"
        "Only output the JSON object, no additional text."
    )

    return [{"role": "system", "content": system}, {"role": "user", "content": "\n".join(user_parts)}]


PROMPT_BUILDERS = {
    ("common_sense", "correction"): common_sense_correction,
    ("common_sense", "wo_correction"): common_sense_wo_correction,
}
