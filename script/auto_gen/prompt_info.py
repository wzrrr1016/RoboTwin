from typing import List, Dict
import json


# We intentionally do not include any prior generated tasks in context.


def _format_selected(containers: List[str], objects: List[str]) -> str:
    return (
        "Selected containers: " + ", ".join(containers) + "\n" +
        "Selected objects (may include duplicates): " + ", ".join(objects)
    )


def _ex_common_sense_correction() -> str:
    ex1 = {
        "task_name": "sort_tool_and_food_correction",
        "task_description": (
            "scene: On the table there are a hamburger, a bread, a hammer, a plate, a wooden_box, plus one extra item (can) that should remain untouched./"
            "task: Put the tool into the wooden_box and put the foods on the plate./"
            "action: First intentionally place the hamburger into the wooden_box (wrong); then correct by moving the hamburger onto the plate. Next place the bread on the plate and place the hammer into the wooden_box."
        ),
    }
    ex2 = {
        "task_name": "commonsense_grouping_correction",
        "task_description": (
            "scene: On the table, there are two cup_without_handle, a yellow block, a toycar, an apple, and a fluted_block./"
            "task: Put non-food items into the fluted_block and keep foods off it./"
            "action: First accidentally grasp the apple and put it on the fluted_block (wrong); then correct by putting the apple back on the table. Next place the two cup_without_handle, the yellow block and the toycar into the fluted_block."
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
        "task_name": "commonsense_grouping_correction",
        "task_description": (
            "scene: On the table, there are two cup_without_handle, a yellow block, a toycar, an apple, and a fluted_block./"
            "task: By everyday rules, put non-food items into the fluted_block and keep foods off it./"
            "action: Place the two cup_without_handle, the yellow block and the toycar into the fluted_block."
        ),
    }
    return json.dumps(ex1, ensure_ascii=False) + "\n" + json.dumps(ex2, ensure_ascii=False)


def common_sense_correction(previous_descs: List[str], selected_containers: List[str], selected_objects: List[str]) -> List[Dict[str, str]]:
    print("selected_containers:", selected_containers)
    print("selected_objects:", selected_objects)
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "You need to design tasks that needs COMMON SENSE reasoning. Incorporate complex everyday reasoning directly into the 'task:' phrasing.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY the selected items listed below; do not invent new items.\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: correction. The task MUST explicitly require making ONE intentional mistake and then recovering. The mistake may occur at ANY step.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- The object must be placed on the containers or the table.\n"
        "- Make tasks complex and multi-step, combining multiple common-sense rules (e.g., tool, food, liquid, solid, shape, fragile, durable, color, healthy, etc.).\n"
        "- Do NOT just describe the steps in the 'task:'; instead, embed common-sense reasoning implicitly like: \"place healthy food\" instead of \"place apple\" .\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    )

    user = (
        _format_selected(selected_containers, selected_objects) + "\n\n" +
        "Design ONE new common_sense task now using ONLY the selected items.\n"
        "Return only one line of JSON in the exact format.\n"
        "examples (each line is a JSON example; do not reuse):\n"
        f"{_ex_common_sense_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def common_sense_wo_correction(previous_descs: List[str], selected_containers: List[str], selected_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "You need to design tasks that needs COMMON SENSE reasoning. Incorporate complex everyday reasoning directly into the 'task:' phrasing.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY the selected items listed below; do not invent new items.\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: wo_correction. Do NOT include any intentional mistake or recovery.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- The object must be placed on the containers or the table.\n"
        "- Make tasks complex and multi-step, combining multiple common-sense rules (e.g., tool, food, liquid, solid, shape, durable, color, healthy, etc.).\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    )

    user = (
        _format_selected(selected_containers, selected_objects) + "\n\n" +
        "Design ONE new common_sense task now using ONLY the selected items.\n"
        "Return only one line of JSON in the exact format.\n"
        "examples (each line is a JSON example; do not reuse):\n"
        f"{_ex_common_sense_wo_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


PROMPT_BUILDERS = {
    ("common_sense", "correction"): common_sense_correction,
    ("common_sense", "wo_correction"): common_sense_wo_correction,
}
