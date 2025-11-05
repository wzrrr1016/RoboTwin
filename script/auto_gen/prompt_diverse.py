from typing import List, Dict
import json
import random


def _format_selected(containers: List[str], objects: List[str]) -> str:
    return (
        "Candidate containers: " + ", ".join(containers) + "\n" +
        "Candidate objects: " + ", ".join(objects)
    )


# Extended attribute knowledge base
ATTR_KB: Dict[str, List[str]] = {
    # foods and nutrition
    "apple": ["food", "healthy", "red", "round", "natural", "fruit", "edible", "organic", "perishable"],
    "bread": ["food", "fermented", "grain", "carbohydrate", "edible", "soft", "perishable"],
    "hamburg": ["food", "unhealthy", "has_bread", "fermented", "contains_meat", "processed", "fast_food", "edible"],
    "french_fries": ["food", "unhealthy", "fried", "yellow", "fast_food", "hot", "oily", "edible"],

    # drinkware / liquid holders and handles
    "bottle": ["liquid_container", "no_handle", "transparent", "plastic_or_glass", "portable", "drinkware", "recyclable"],
    "cup": ["liquid_container", "unknown_handle", "drinkware", "for_drinking"],
    "cup_with_handle": ["liquid_container", "has_handle", "drinkware", "for_hot_drinks", "easy_to_hold"],
    "cup_without_handle": ["liquid_container", "no_handle", "drinkware", "for_cold_drinks", "hard_to_hold_when_hot"],
    "mug": ["liquid_container", "has_handle", "drinkware", "for_hot_drinks", "ceramic"],
    "can": ["liquid_container", "metal", "no_handle", "sealed", "cylindrical", "drinkware", "recyclable"],

    # tableware and danger
    "knife": ["tableware", "dangerous", "sharp", "metal", "cutting_tool", "requires_care"],
    "fork": ["tableware", "metal", "for_eating", "has_prongs", "safe"],

    # tools / repair / office
    "screwdriver": ["tool", "repair", "metal", "hand_tool", "for_screws", "maintenance"],
    "drill": ["tool", "repair", "electric", "power_tool", "for_holes", "maintenance", "heavy"],
    "stapler": ["tool", "office", "metal", "for_paper", "binding_tool"],
    "scanner": ["electronic", "office", "for_documents", "digital", "stationary"],
    "mouse": ["electronic", "office", "computer_accessory", "plastic", "handheld"],
    "hammer": ["tool", "repair", "metal", "hand_tool", "for_striking", "heavy"],

    # toys / decor
    "toycar": ["toy", "wheels", "for_children", "entertainment", "movable", "plastic"],
    "pot-with-plant": ["plant", "decor", "green", "living", "needs_water", "decorative", "natural", "organic"],

    # time / sound utilities
    "alarm-clock": ["time", "sound", "electronic", "wakes_up", "displays_time", "makes_noise"],
    "sand-clock": ["time", "no_sound", "analog", "visual", "passive", "decorative"],
    "microphone": ["sound", "audio_input", "electronic", "for_recording", "captures_sound"],
    "bell": ["sound", "audio_output", "metal", "for_alerting", "produces_sound", "ringing"],

    # cleaning / bath / weight
    "tissue-box": ["cleaning", "paper", "disposable", "for_wiping", "hygiene", "single_use", "recyclable"],
    "shampoo": ["bath", "liquid", "hygiene", "for_hair", "personal_care", "consumable", "bottle_container"],
    "dumbbell": ["heavy", "metal", "exercise", "fitness", "weight_training", "solid"],

    # clothing
    "shoe": ["clothing", "footwear", "wearable", "protective", "for_feet", "outdoor"],

    # reading / material
    "book": ["reading", "wood_material", "paper", "educational", "rectangular", "has_pages", "knowledge", "recyclable"],
    "teanet": ["tea", "kitchen", "for_tea", "mesh", "strainer"],

    # colored square blocks (RGB color model)
    "red_block": ["block", "red", "primary_color", "square", "solid", "toy_or_tool"],
    "green_block": ["block", "green", "primary_color", "square", "solid", "toy_or_tool"],
    "blue_block": ["block", "blue", "primary_color", "square", "solid", "toy_or_tool"],
    "yellow_block": ["block", "yellow", "secondary_color", "square", "solid", "toy_or_tool"],
    "purple_block": ["block", "purple", "secondary_color", "square", "solid", "toy_or_tool"],
    "orange_block": ["block", "orange", "tertiary_color", "square", "solid", "toy_or_tool"],
    "pink_block": ["block", "pink", "tint", "square", "solid", "toy_or_tool"],
}

# Container attributes
CONTAINER_KB: Dict[str, List[str]] = {
    "plate": ["container", "food_surface", "flat", "circular", "for_food", "kitchen", "ceramic"],
    "tray": ["container", "group_surface", "flat", "rectangular", "for_organization", "holds_multiple_items"],
    "wooden_box": ["container", "storage", "enclosed", "wood", "for_general_items", "has_lid"],
    "dustbin": ["container", "waste", "for_trash", "disposal", "unwanted_items", "recyclable_items"],
    "fluted_block": ["container", "group_surface", "flat", "for_organization", "stable_base"],
    "shoe_box": ["container", "for_shoe", "enclosed", "specific_purpose", "storage", "rectangular"],
    "coaster": ["container", "for_drinkware", "flat", "protects_surface", "for_cups_and_mugs"],
}

# Color theory (RGB additive color model - mixing outcomes)
COLOR_MIX = {
    "red+green": "yellow",      # primary + primary = secondary
    "red+blue": "purple",        # primary + primary = secondary (magenta)
    "red+yellow": "orange",      # primary + secondary = tertiary
}


def _format_attribute_sheet(containers: List[str], objects: List[str]) -> str:
    lines: List[str] = []
    lines.append("Attributes (use for reasoning, do not invent):")
    for c in containers:
        lines.append(f"- {c}: " + ", ".join(CONTAINER_KB.get(c, ["container"])))
    for o in objects:
        tags = ATTR_KB.get(o, [])
        if tags:
            lines.append(f"- {o}: " + ", ".join(tags))
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
        "task_description": (
            "scene: Containers: plate, wooden_box. Objects: apple, hamburg, french_fries,toycar./"
            "task: Put the healthy items into the plate and unhealthy items into the wooden_box./"
            "action: Pick apple and place into wooden_box (wrong). Pick apple from wooden_box and place into plate (recovery). Pick hamburg and place into wooden_box. Pick french_fries and place into wooden_box."
        ),
    }
    ex2 = {
        "task_name": "liquid_container_grouping_correction",
        "task_description": (
            "scene: Containers: coaster, dustbin. Objects: bottle, cup_with_handle, mug,book./"
            "task: Put drinkware with handles into the coaster and those without handles into the dustbin./"
            "action: Pick bottle and place into coaster (wrong). Pick bottle from coaster and place into dustbin (recovery). Pick cup_with_handle and place into coaster. Pick mug and place into coaster."
        ),
    }
    return json.dumps(ex1, ensure_ascii=False) + "\n" + json.dumps(ex2, ensure_ascii=False)


def _examples_wo_correction() -> str:
    ex1 = {
        "task_name": "shoe_storage_task",
        "task_description": (
            "scene: Containers: shoe_box, wooden_box. Objects: shoe, screwdriver./"
            "task: Put footwear items into their designated storage and repair tools into general storage./"
            "action: Pick shoe and place into shoe_box. Pick screwdriver and place into wooden_box."
        ),
    }
    ex2 = {
        "task_name": "time_utility_organization",
        "task_description": (
            "scene: Containers: tray, dustbin. Objects: alarm-clock, sand-clock, bell./"
            "task: Put time-related items into the tray and sound-only items into the dustbin./"
            "action: Pick alarm-clock and place into tray. Pick sand-clock and place into tray. Pick bell and place into dustbin."
        ),
    }
    return json.dumps(ex1, ensure_ascii=False) + "\n" + json.dumps(ex2, ensure_ascii=False)


def _system_block(mode: str) -> str:
    if mode == "correction":
        return (
            "Design a pick-place task with common sense reasoning and ONE mistake that gets corrected.\n"
            "Output: {'task_name': '...', 'task_description': 'scene: .../task: .../action: ...'}\n\n"
            "Requirements:\n"
            "- Use ONLY provided candidates (1-2 containers, 3-5 objects)\n"
            "- IMPORTANT: Total items (containers + objects) must NOT exceed 7\n"
            "- scene: MUST use format 'scene: Containers: X, Y. Objects: A, B, C./' (clearly separate containers and objects)\n"
            "  * Can include 0-2 distractor objects (items not involved in the task)\n"
            "- task: Use category descriptions requiring reasoning (e.g., 'Put healthy foods into plate')\n"
            "  * NO specific item names, NO vague phrases like 'arrange by color'\n"
            "  * Must specify target containers clearly\n"
            "- action: Use format 'Pick X and place into/on Y'\n"
            "  * Include ONE mistake: either wrong container OR wrong object (distractor)\n"
            "  * Mark mistake with '(wrong)', then correct it with '(recovery)'\n"
            "  * If wrong object: 'Pick X and place on table' to put it back\n"
            "  * Mistake can occur at any step, not just first\n"
            "  * MAXIMUM 5 pick-place operations (including correction)\n"
            "\n"
            "Knowledge:\n"
            "• apple=healthy; hamburg,french_fries=unhealthy\n"
            "• mug,cup_with_handle=has_handle; bottle,cup_without_handle=no_handle\n"
            "• knife=dangerous; screwdriver,drill,hammer=repair; stapler,scanner,mouse=office\n"
            "• alarm-clock=time+sound; sand-clock=time; bell,microphone=sound\n"
            "• RGB color model: red/green/blue=primary; yellow/purple=secondary; orange=tertiary\n"
            "• Color mixing: red+green=yellow, red+blue=purple, red+yellow=orange\n"
        )
    else:
        return (
            "Design a pick-place task with common sense reasoning.\n"
            "Output: {'task_name': '...', 'task_description': 'scene: .../task: .../action: ...'}\n\n"
            "Requirements:\n"
            "- Use ONLY provided candidates (1-2 containers, 3-5 objects)\n"
            "- IMPORTANT: Total items (containers + objects) must NOT exceed 7\n"
            "- scene: MUST use format 'scene: Containers: X, Y. Objects: A, B, C./' (clearly separate containers and objects)\n"
            "  * Can include 0-2 distractor objects (items not involved in the task)\n"
            "- task: Use category descriptions requiring reasoning (e.g., 'Put healthy foods into plate')\n"
            "  * NO specific item names, NO vague phrases like 'arrange by color'\n"
            "  * Must specify target containers clearly\n"
            "- action: Use format 'Pick X and place into/on Y'\n"
            "  * MAXIMUM 5 pick-place operations\n"
            "  * All actions correct, NO mistakes\n"
            "\n"
            "Knowledge:\n"
            "• apple=healthy; hamburg,french_fries=unhealthy\n"
            "• mug,cup_with_handle=has_handle; bottle,cup_without_handle=no_handle\n"
            "• knife=dangerous; screwdriver,drill,hammer=repair; stapler,scanner,mouse=office\n"
            "• alarm-clock=time+sound; sand-clock=time; bell,microphone=sound\n"
            "• RGB color model: red/green/blue=primary; yellow/purple=secondary; orange=tertiary\n"
            "• Color mixing: red+green=yellow, red+blue=purple, red+yellow=orange\n"
        )


def common_sense_diverse(previous_descs: List[str], selected_containers: List[str],
                        selected_objects: List[str], mode: str) -> List[Dict[str, str]]:
    system = _system_block(mode)
    recent = _recent_summaries(previous_descs)
    attr_sheet = _format_attribute_sheet(selected_containers, selected_objects)

    user = (
        _format_selected(selected_containers, selected_objects) + "\n\n" +
        attr_sheet + "\n\n" +
        "Recent tasks (avoid similar):\n" + recent + "\n\n" +
        "Design ONE new task using ONLY candidates above. Return one JSON line.\n"
        "Examples:\n" +
        (_examples_correction() if mode == "correction" else _examples_wo_correction())
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def common_sense_correction(previous_descs: List[str], selected_containers: List[str],
                           selected_objects: List[str]) -> List[Dict[str, str]]:
    return common_sense_diverse(previous_descs, selected_containers, selected_objects, mode="correction")


def common_sense_wo_correction(previous_descs: List[str], selected_containers: List[str],
                               selected_objects: List[str]) -> List[Dict[str, str]]:
    return common_sense_diverse(previous_descs, selected_containers, selected_objects, mode="wo_correction")


PROMPT_BUILDERS = {
    ("common_sense", "correction"): common_sense_correction,
    ("common_sense", "wo_correction"): common_sense_wo_correction,
}
