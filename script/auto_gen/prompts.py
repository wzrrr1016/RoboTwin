from typing import List, Dict
import json

# ---------------- Category-specific example builders ----------------
def _ex_common_sense_correction() -> str:
    ex = {
        "task_name": "cs_commonsense_correction_example",
        "task_description": (
            "scene: On the table there are an apple, a bread, a hamburg, a hammer, a bottle, a plate, a tray, a wooden_box, plus extra items (can, toycar) that should remain untouched./"
            "reasoning: Combine everyday rules: tools belong in the wooden_box; solid foods go on the plate; liquid containers should be placed on the tray. Avoid moving extra items (can, toycar). The plan must contain multiple steps and justify why each item fits its destination./"
            "task: Put the hammer into the wooden_box; place the apple, bread, and hamburg on the plate; place the bottle on the tray; do not move the can or the toycar./"
            "action: First intentionally place the apple into the wooden_box (wrong); then correct by moving the apple onto the plate. Next place the bread on the plate, the hamburg on the plate, the hammer into the wooden_box, and the bottle onto the tray."
        ),
    }
    return json.dumps(ex, ensure_ascii=False)


def _ex_common_sense_wo_correction() -> str:
    ex = {
        "task_name": "cs_commonsense_example",
        "task_description": (
            "scene: On the table there are an apple, a bread, a hamburg, a hammer, a bottle, a plate, a tray, a wooden_box, plus extra items (can, toycar) that should remain untouched./"
            "reasoning: Combine everyday rules: tools belong in the wooden_box; solid foods go on the plate; liquid containers should be placed on the tray. Avoid moving extra items (can, toycar). Provide multi-step justification for placements./"
            "task: Put the hammer into the wooden_box; place the apple, bread, and hamburg on the plate; place the bottle on the tray; do not move the can or the toycar./"
            "action: Place the hammer into the wooden_box, place the apple on the plate, place the bread on the plate, place the hamburg on the plate, and place the bottle on the tray."
        ),
    }
    return json.dumps(ex, ensure_ascii=False)


def _ex_counting_correction() -> str:
    ex = {
        "task_name": "counting_composite_correction_example",
        "task_description": (
            "scene: On the table there are four red_block, three blue_block, two green_block, a bowl, a plate, a tray, plus extra items (bottle, can) that should remain untouched./"
            "reasoning: Use composite counting: place exactly three red_block on the tray; exactly two green_block inside the bowl; exactly one blue_block on the plate. Ensure the total moved blocks equals six and color constraints are satisfied. Provide step-wise numeric justification./"
            "task: Put three red_block on the tray, two green_block inside the bowl, and one blue_block on the plate; do not move the bottle or the can./"
            "action: First intentionally put one blue_block inside the bowl (wrong); then correct by removing that blue_block back to the table. Next place three red_block on the tray, place two green_block inside the bowl, and place one blue_block on the plate."
        ),
    }
    return json.dumps(ex, ensure_ascii=False)


def _ex_counting_wo_correction() -> str:
    ex = {
        "task_name": "counting_composite_example",
        "task_description": (
            "scene: On the table there are four red_block, three blue_block, two green_block, a bowl, a plate, a tray, plus extra items (bottle, can) that should remain untouched./"
            "reasoning: Use composite counting: place exactly three red_block on the tray; exactly two green_block inside the bowl; exactly one blue_block on the plate. Ensure the total moved blocks equals six and color constraints are satisfied. Provide step-wise numeric justification./"
            "task: Put three red_block on the tray, two green_block inside the bowl, and one blue_block on the plate; do not move the bottle or the can./"
            "action: Place three red_block on the tray, place two green_block inside the bowl, and place one blue_block on the plate."
        ),
    }
    return json.dumps(ex, ensure_ascii=False)


def _ex_spatial_correction() -> str:
    ex = {
        "task_name": "spatial_multi_relations_correction_example",
        "task_description": (
            "scene: On the table there are a cup, a plate, a bowl, a tray, a toycar, plus extra items (bottle, can) that should remain untouched./"
            "reasoning: Combine spatial rules: the cup must be to the left of the plate; the toycar must be inside the bowl; the bottle should be placed on the tray. Justify each relation and ensure extra items (can) remain unmoved./"
            "task: Put the cup to the left of the plate; put the toycar inside the bowl; put the bottle on the tray; do not move the can./"
            "action: First intentionally put the cup to the right of the plate (wrong); then correct by moving the cup to the left of the plate. Next put the toycar inside the bowl and put the bottle on the tray."
        ),
    }
    return json.dumps(ex, ensure_ascii=False)


def _ex_spatial_wo_correction() -> str:
    ex = {
        "task_name": "spatial_multi_relations_example",
        "task_description": (
            "scene: On the table there are a cup, a plate, a bowl, a tray, a toycar, plus extra items (bottle, can) that should remain untouched./"
            "reasoning: Combine spatial rules: the cup must be to the left of the plate; the toycar must be inside the bowl; the bottle should be placed on the tray. Justify each relation and ensure extra items (can) remain unmoved./"
            "task: Put the cup to the left of the plate; put the toycar inside the bowl; put the bottle on the tray; do not move the can./"
            "action: Put the cup to the left of the plate, put the toycar inside the bowl, and put the bottle on the tray."
        ),
    }
    return json.dumps(ex, ensure_ascii=False)


def _ctx_block(previous_descs: List[str]) -> str:
    if not previous_descs:
        return "No prior descriptions."
    lines = "\n".join([f"- {d}" for d in previous_descs])
    return f"Existing task descriptions (do not repeat any):\n{lines}"


def _objects_block(available_objects: List[str]) -> str:
    return json.dumps(available_objects, ensure_ascii=False)


def common_sense_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: common_sense. The task_description must include a 'reasoning:' segment that explicitly describes the commonsense used.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../reasoning: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: correction. The task MUST explicitly require making ONE intentional mistake and then recovering.\n"
        "  In the action, first perform the wrong step, then undo/restore and finish correctly.\n"
        "- The scene MUST include at least two additional objects that remain untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Do NOT use the word 'sort' in 'task_name'.\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now.\n"
        "Return only one line of JSON in the exact format.\n"
        f"Category-specific example (do not reuse): {_ex_common_sense_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def common_sense_wo_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: common_sense. The task_description must include a 'reasoning:' segment that explicitly describes the commonsense used.\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../reasoning: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: wo_correction. Do NOT include any intentional mistake or recovery.\n"
        "- The scene MUST include at least two additional objects that remain untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Do NOT use the word 'sort' in 'task_name'.\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now\n"
        "Return only one line of JSON in the exact format.\n"
        f"Category-specific example (do not reuse): {_ex_common_sense_wo_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def counting_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: counting. The task_description must include a 'reasoning:' segment that explains the counting logic (exact counts/colors).\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../reasoning: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: correction. The task MUST explicitly require making ONE intentional mistake and then recovering.\n"
        "  In the action, first perform the wrong step, then undo/restore and finish correctly.\n"
        "- The scene MUST include at least two additional objects that remain untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Do NOT use the word 'sort' in 'task_name'.\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now (counting: exact numbers and colors).\n"
        "Return only one line of JSON in the exact format.\n"
        f"Category-specific example (do not reuse): {_ex_counting_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def counting_wo_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: counting. The task_description must include a 'reasoning:' segment that explains the counting logic (exact counts/colors).\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../reasoning: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: wo_correction. Do NOT include any intentional mistake or recovery.\n"
        "- The scene MUST include at least two additional objects that remain untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Do NOT use the word 'sort' in 'task_name'.\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now (counting: exact numbers and colors).\n"
        "Return only one line of JSON in the exact format.\n"
        f"Category-specific example (do not reuse): {_ex_counting_wo_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def spatial_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: spatial. The task_description must include a 'reasoning:' segment that explains the spatial rule (left/right/inside/on/near).\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../reasoning: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: correction. The task MUST explicitly require making ONE intentional mistake and then recovering.\n"
        "  In the action, first perform the wrong step, then undo/restore and finish correctly.\n"
        "- The scene MUST include at least two additional objects that remain untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Do NOT use the word 'sort' in 'task_name'.\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now (spatial: explicit relations like left/right/inside/on/near).\n"
        "Return only one line of JSON in the exact format.\n"
        f"Category-specific example (do not reuse): {_ex_spatial_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def spatial_wo_correction(previous_descs: List[str], available_objects: List[str]) -> List[Dict[str, str]]:
    system = (
        "You are an expert tabletop manipulation task designer.\n"
        "Reasoning type: spatial. The task_description must include a 'reasoning:' segment that explains the spatial rule (left/right/inside/on/near).\n"
        "Output a SINGLE-LINE JSON with exactly two keys: 'task_name' and 'task_description'.\n"
        "The 'task_description' must strictly follow: 'scene: .../reasoning: .../task: .../action: ...'.\n"
        "Constraints:\n"
        "- Use ONLY these object names (exact match): {objects}\n"
        "- No extra fields, no code blocks, no backticks.\n"
        "- Mode: wo_correction. Do NOT include any intentional mistake or recovery.\n"
        "- The scene MUST include at least two additional objects that remain untouched in 'action'.\n"
        "- The 'action' MUST include at least three distinct pick-and-place operations.\n"
        "- Do NOT use the word 'sort' in 'task_name'.\n"
        "- The new description must not duplicate or closely paraphrase any prior description in the context.\n"
    ).replace("{objects}", _objects_block(available_objects))

    user = (
        _ctx_block(previous_descs) + "\n\n"
        "Design ONE new task now (spatial: explicit relations like left/right/inside/on/near).\n"
        "Return only one line of JSON in the exact format.\n"
        f"Category-specific example (do not reuse): {_ex_spatial_wo_correction()}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


# Dispatcher utility
PROMPT_BUILDERS = {
    ("common_sense", "correction"): common_sense_correction,
    ("common_sense", "wo_correction"): common_sense_wo_correction,
    ("counting", "correction"): counting_correction,
    ("counting", "wo_correction"): counting_wo_correction,
    ("spatial", "correction"): spatial_correction,
    ("spatial", "wo_correction"): spatial_wo_correction,
}
