from typing import List, Dict
import json


def _objects_block(items: List[str]) -> str:
    return ", ".join(sorted(set(items)))


def _ex_common_sense_correction() -> str:
    ex1 = {
        "task_name": "sort_tool_and_food_correction",
        "task_description": (
            "scene: On the table there are a hamburger, a bread, a hammer, a plate, a wooden_box, plus one extra item (can) that should remain untouched./"
            "task: Put the tool into the wooden_box and put the foods on the plate./"
            "action: Make one intentional mistake at any step: e.g., place the hamburger into the wooden_box (wrong); then correct by moving the hamburger onto the plate. Next place the bread on the plate and place the hammer into the wooden_box."
        ),
    }
    ex2 = {
        "task_name": "commonsense_grouping_correction",
        "task_description": (
            "scene: On the table, there are two cup_without_handle, a bread, a toycar, an apple, and a fluted_block./"
            "task: By everyday rules, put non-food items into the fluted_block and keep foods off it./"
            "action: Make one intentional mistake at any step: e.g., put the apple on the fluted_block (wrong); then correct by returning the apple to the table. Next place the two cup_without_handle and the toycar into the fluted_block."
        ),
    }
    return json.dumps(ex1, ensure_ascii=False) + "\n" + json.dumps(ex2, ensure_ascii=False)


def _ex_common_sense_wo_correction() -> str:
    ex1 = {
        "task_name": "commonsense_example",
        "task_description": (
            "scene: On the table there are an apple, a bread, a hammer, a plate, a wooden_box, plus one extra item (toycar) that should remain untouched./"
            "task: Put the tool into the wooden_box and put the foods on the plate./"
            "action: Place the hammer into the wooden_box, place the apple on the plate, and place the bread on the plate."
        ),
    }
    ex2 = {
        "task_name": "commonsense_example_variant",
        "task_description": (
            "scene: On the table there are a hamburg, a bread, a screwdriver, a tray, a wooden_box, plus one extra item (can) that should remain untouched./"
            "task: Put the tool into the wooden_box and put the foods on the tray./"
            "action: Place the screwdriver into the wooden_box, place the hamburg on the tray, and place the bread on the tray."
        ),
    }
    return json.dumps(ex1, ensure_ascii=False) + "\n" + json.dumps(ex2, ensure_ascii=False)


def common_sense_correction(previous_descs: List[str], full_containers: List[str], full_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: common_sense. Incorporate complex everyday reasoning directly into the 'task:' phrasing; do NOT include an explicit 'reasoning:' segment.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Select 1–2 containers from the list and 4–6 objects (duplicates allowed) from the list; use ONLY selected items in the task.\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: correction. The task MUST explicitly require making ONE intentional mistake and then recovering. The mistake may occur at ANY step, not necessarily the first.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Make tasks complex and multi-step, combining multiple common-sense rules (e.g., tool vs. food, liquid vs. solid, fragile vs. durable).\n"
    )

    user = (
        "Available containers: " + _objects_block(full_containers) + "\n"
        "Available objects: " + _objects_block(full_objects) + "\n\n"
        "Choose items and design ONE new common_sense task using ONLY your selected items.\n"
        "Return only one line of JSON in the exact format.\n"
        "Category-specific examples (each line is a JSON example; do not reuse):\n"
        f"{_ex_common_sense_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def common_sense_wo_correction(previous_descs: List[str], full_containers: List[str], full_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: common_sense. Incorporate complex everyday reasoning directly into the 'task:' phrasing; do NOT include an explicit 'reasoning:' segment.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Select 1–2 containers from the list and 4–6 objects (duplicates allowed) from the list; use ONLY selected items in the task.\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: wo_correction. Do NOT include any intentional mistake or recovery.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Make tasks complex and multi-step, combining multiple common-sense rules (e.g., tool vs. food, liquid vs. solid, fragile vs. durable).\n"
    )

    user = (
        "Available containers: " + _objects_block(full_containers) + "\n"
        "Available objects: " + _objects_block(full_objects) + "\n\n"
        "Choose items and design ONE new common_sense task using ONLY your selected items.\n"
        "Return only one line of JSON in the exact format.\n"
        "Category-specific examples (each line is a JSON example; do not reuse):\n"
        f"{_ex_common_sense_wo_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


PROMPT_BUILDERS = {
    ("common_sense", "correction"): common_sense_correction,
    ("common_sense", "wo_correction"): common_sense_wo_correction,
}

