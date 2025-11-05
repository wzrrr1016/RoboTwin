from typing import List, Dict
import json


def _ctx_block(previous_descs: List[str]) -> str:
    if not previous_descs:
        return "No prior tasks in context."
    head = [f"- {d}" for d in previous_descs[-10:]]
    return "Previously generated tasks (do not duplicate or paraphrase):\n" + "\n".join(head)


def _objects_block(available_objects: List[str]) -> str:
    return ", ".join(sorted(set(available_objects)))


# ---------------- Category-specific example builders (3 operated + 1 untouched) ----------------
def _ex_common_sense_correction() -> str:
    ex = {
        "task_name": "sort_tool_and_food_correction",
        "task_description": (
            "scene: On the table there are a hamburger, a bread, a hammer, a plate, a wooden_box, plus one extra item (can) that should remain untouched./"
            "task: Put the tool into the wooden_box and put the foods on the plate./"
            "action: First intentionally place the hamburger into the wooden_box (wrong); then correct by moving the hamburger onto the plate. Next place the bread on the plate and place the hammer into the wooden_box."
        ),
    }
    ex1 = {
        "task_name": "commonsense_grouping_correction",
        "task_description": (
            "scene: On the table, there are two cup_without_handle, a yellow block, a toycar, an apple, and a fluted_block./"
            "task: By everyday rules, put non-food items into the fluted_block and keep foods off it./"
            "action: First accidentally grasp the apple and put it on the fluted_block (wrong); then correct by putting the apple back on the table. Next place the two cup_without_handle, the yellow block and the toycar into the fluted_block."
        ),
    }
    return json.dumps(ex, ensure_ascii=False) + "\n" + json.dumps(ex1, ensure_ascii=False)


def _ex_common_sense_wo_correction() -> str:
    ex = {
        "task_name": "commonsense_example",
        "task_description": (
            "scene: On the table there are an apple, a bread, a hammer, a plate, a wooden_box, plus one extra item (toycar) that should remain untouched./"
            "task: Put the tool into the wooden_box and put the foods on the plate./"
            "action: Place the hammer into the wooden_box, place the apple on the plate, and place the bread on the plate."
        ),
    }
    ex1 = {
        "task_name": "commonsense_example_variant",
        "task_description": (
            "scene: On the table there are a hamburg, a bread, a screwdriver, a tray, a wooden_box, plus one extra item (can) that should remain untouched./"
            "task: Put the tool into the wooden_box and put the foods on the tray./"
            "action: Place the screwdriver into the wooden_box, place the hamburg on the tray, and place the bread on the tray."
        ),
    }
    return json.dumps(ex, ensure_ascii=False) + "\n" + json.dumps(ex1, ensure_ascii=False)


def _ex_counting_correction() -> str:
    ex = {
        "task_name": "counting_composite_correction_example",
        "task_description": (
            "scene: On the table there are two red_block, one green_block, a wooden_box, a tray, plus one extra item (bottle) that should remain untouched./"
            "task: Using counting rules, place exactly two red_block on the tray and put the single green_block inside the wooden_box; do not move the bottle./"
            "action: First intentionally put the green_block on the tray (wrong); then correct by moving the green_block into the wooden_box. Next place one red_block on the tray and place the other red_block on the tray."
        ),
    }
    ex1 = {
        "task_name": "counting_composite_correction_variant",
        "task_description": (
            "scene: On the table there are two red_block, one green_block, a wooden_box, a plate, plus one extra item (bottle) that should remain untouched./"
            "task: Using counting rules, place exactly two red_block on the plate and put the single green_block inside the wooden_box; do not move the bottle./"
            "action: First intentionally put one red_block inside the wooden_box (wrong); then correct by removing that red_block back to the table. Next place two red_block on the plate and place the green_block inside the wooden_box."
        ),
    }
    return json.dumps(ex, ensure_ascii=False) + "\n" + json.dumps(ex1, ensure_ascii=False)


def _ex_counting_wo_correction() -> str:
    ex = {
        "task_name": "counting_composite_example",
        "task_description": (
            "scene: On the table there are two red_block, one green_block, a wooden_box, a tray, plus one extra item (bottle) that should remain untouched./"
            "task: Using counting rules, place exactly two red_block on the tray and put the single green_block inside the wooden_box; do not move the bottle./"
            "action: Place one red_block on the tray, place the other red_block on the tray, and place the green_block inside the wooden_box."
        ),
    }
    ex1 = {
        "task_name": "counting_composite_example_variant",
        "task_description": (
            "scene: On the table there are two red_block, one green_block, a wooden_box, a plate, plus one extra item (bottle) that should remain untouched./"
            "task: Using counting rules, place exactly two red_block on the plate and put the single green_block inside the wooden_box; do not move the bottle./"
            "action: Place one red_block on the plate, place the other red_block on the plate, and place the green_block inside the wooden_box."
        ),
    }
    return json.dumps(ex, ensure_ascii=False) + "\n" + json.dumps(ex1, ensure_ascii=False)


def _ex_spatial_correction() -> str:
    ex = {
        "task_name": "spatial_multi_relations_correction_example",
        "task_description": (
            "scene: On the table there are a cup, a bottle, a toycar, a plate, a wooden_box, plus one extra item (can) that should remain untouched./"
            "task: Using spatial relations, ensure the cup is to the left of the plate, put the toycar inside the wooden_box, and place the bottle on the plate; do not move the can./"
            "action: First intentionally put the cup to the right of the plate (wrong); then correct by moving the cup to the left of the plate. Next put the toycar inside the wooden_box and place the bottle on the plate."
        ),
    }
    ex1 = {
        "task_name": "spatial_multi_relations_correction_variant",
        "task_description": (
            "scene: On the table there are a mug, a bottle, a toycar, a tray, a wooden_box, plus one extra item (can) that should remain untouched./"
            "task: Using spatial relations, ensure the mug is to the left of the tray, put the toycar inside the wooden_box, and place the bottle on the tray; do not move the can./"
            "action: First intentionally put the mug to the right of the tray (wrong); then correct by moving the mug to the left of the tray. Next put the toycar inside the wooden_box and place the bottle on the tray."
        ),
    }
    return json.dumps(ex, ensure_ascii=False) + "\n" + json.dumps(ex1, ensure_ascii=False)


def _ex_spatial_wo_correction() -> str:
    ex = {
        "task_name": "spatial_multi_relations_example",
        "task_description": (
            "scene: On the table there are a cup, a bottle, a toycar, a plate, a wooden_box, plus one extra item (can) that should remain untouched./"
            "task: Using spatial relations, ensure the cup is to the left of the plate, put the toycar inside the wooden_box, and place the bottle on the plate; do not move the can./"
            "action: Move the cup to the left of the plate, put the toycar inside the wooden_box, and place the bottle on the plate."
        ),
    }
    ex1 = {
        "task_name": "spatial_multi_relations_example_variant",
        "task_description": (
            "scene: On the table there are a mug, a bottle, a toycar, a tray, a wooden_box, plus one extra item (can) that should remain untouched./"
            "task: Using spatial relations, ensure the mug is to the left of the tray, put the toycar inside the wooden_box, and place the bottle on the tray; do not move the can./"
            "action: Move the mug to the left of the tray, put the toycar inside the wooden_box, and place the bottle on the tray."
        ),
    }
    return json.dumps(ex, ensure_ascii=False) + "\n" + json.dumps(ex1, ensure_ascii=False)


# ---------------- Prompt builders ----------------
def common_sense_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: common_sense. Incorporate the reasoning into the 'task:' phrasing; do NOT include an explicit 'reasoning:' segment.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: correction. The task MUST explicitly require making ONE intentional mistake and then recovering.\n"
        "- In the scene, include AT MOST two containers (e.g., plate, tray, wooden_box, dustbin, fluted_block, shoe_box, coaster).\n"
        "- Limit non-container objects to NO MORE THAN six in total.\n"
        "- Include exactly ONE additional object that remains untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Make tasks moderately complex and multi-step, guided by common-sense reasoning (implicit).\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now (common_sense).\n"
        "Return only one line of JSON in the exact format.\n"
        "Category-specific examples (each line is a JSON example; do not reuse):\n"
        f"{_ex_common_sense_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def common_sense_wo_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: common_sense. Incorporate the reasoning into the 'task:' phrasing; do NOT include an explicit 'reasoning:' segment.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: wo_correction. Do NOT include any intentional mistake or recovery.\n"
        "- In the scene, include AT MOST two containers (e.g., plate, tray, wooden_box, dustbin, fluted_block, shoe_box, coaster).\n"
        "- Limit non-container objects to NO MORE THAN five in total.\n"
        "- Include exactly ONE additional object that remains untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Make tasks moderately complex and multi-step, guided by common-sense reasoning (implicit).\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now.\n"
        "Return only one line of JSON in the exact format.\n"
        "Category-specific examples (each line is a JSON example; do not reuse):\n"
        f"{_ex_common_sense_wo_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def counting_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: counting. Incorporate the counting logic into the 'task:' phrasing; do NOT include an explicit 'reasoning:' segment.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: correction. The task MUST explicitly require making ONE intentional mistake and then recovering.\n"
        "  In the action, first perform the wrong step, then undo/restore and finish correctly.\n"
        "- In the scene, include AT MOST two containers (e.g., plate, tray, wooden_box, dustbin, fluted_block, shoe_box, coaster).\n"
        "- Limit non-container objects to NO MORE THAN five in total.\n"
        "- Include exactly ONE additional object that remains untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Make tasks moderately complex and multi-step, guided by counting reasoning (implicit).\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now (counting: exact numbers and colors).\n"
        "Return only one line of JSON in the exact format.\n"
        "Category-specific examples (each line is a JSON example; do not reuse):\n"
        f"{_ex_counting_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def counting_wo_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: counting. Incorporate the counting logic into the 'task:' phrasing; do NOT include an explicit 'reasoning:' segment.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: wo_correction. Do NOT include any intentional mistake or recovery.\n"
        "- In the scene, include AT MOST two containers (e.g., plate, tray, wooden_box, dustbin, fluted_block, shoe_box, coaster).\n"
        "- Limit non-container objects to NO MORE THAN five in total.\n"
        "- Include exactly ONE additional object that remains untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Make tasks moderately complex and multi-step, guided by counting reasoning (implicit).\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now (counting: exact numbers and colors).\n"
        "Return only one line of JSON in the exact format.\n"
        "Category-specific examples (each line is a JSON example; do not reuse):\n"
        f"{_ex_counting_wo_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def spatial_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: spatial. Incorporate the spatial logic into the 'task:' phrasing; do NOT include an explicit 'reasoning:' segment.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: correction. The task MUST explicitly require making ONE intentional mistake and then recovering.\n"
        "  In the action, first perform the wrong step, then undo/restore and finish correctly.\n"
        "- In the scene, include AT MOST two containers (e.g., plate, tray, wooden_box, dustbin, fluted_block, shoe_box, coaster).\n"
        "- Limit non-container objects to NO MORE THAN five in total.\n"
        "- Include exactly ONE additional object that remains untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Make tasks moderately complex and multi-step, guided by spatial reasoning (implicit).\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now (spatial: explicit relations like left/right/inside/on/near).\n"
        "Return only one line of JSON in the exact format.\n"
        "Category-specific examples (each line is a JSON example; do not reuse):\n"
        f"{_ex_spatial_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def spatial_wo_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: spatial. Incorporate the spatial logic into the 'task:' phrasing; do NOT include an explicit 'reasoning:' segment.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: wo_correction. Do NOT include any intentional mistake or recovery.\n"
        "- In the scene, include AT MOST two containers (e.g., plate, tray, wooden_box, dustbin, fluted_block, shoe_box, coaster).\n"
        "- Limit non-container objects to NO MORE THAN five in total.\n"
        "- Include exactly ONE additional object that remains untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Make tasks moderately complex and multi-step, guided by spatial reasoning (implicit).\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now (spatial: explicit relations like left/right/inside/on/near).\n"
        "Return only one line of JSON in the exact format.\n"
        "Category-specific examples (each line is a JSON example; do not reuse):\n"
        f"{_ex_spatial_wo_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


PROMPT_BUILDERS = {
    ("common_sense", "correction"): common_sense_correction,
    ("common_sense", "wo_correction"): common_sense_wo_correction,
    ("counting", "correction"): counting_correction,
    ("counting", "wo_correction"): counting_wo_correction,
    ("spatial", "correction"): spatial_correction,
    ("spatial", "wo_correction"): spatial_wo_correction,
}
