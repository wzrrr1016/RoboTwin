'''
Usage:
python script/auto_gen/generate_task_info_diverse.py \
    --categories common_sense \
    --output_dir /home/wangzhuoran/RoboTwin/code_gen/task_info/ \
    --num_per_mode 5 \
    --modes correction \
    --enable_validation
    
'''

import os
import json
import argparse
import random
import re
from typing import Dict, Any, List, Optional, Tuple
import sys

try:
    # When executed as a module: python -m script.auto_gen.generate_task_info_diverse
    from .prompt_diverse import PROMPT_BUILDERS, select_distractors_prompt
    from .all_object import ATTR_KB, CONTAINER_KB, DISTRACTOR_KB
except Exception:
    # When executed as a script: python script/auto_gen/generate_task_info_diverse.py
    _CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    if _CURR_DIR not in sys.path:
        sys.path.append(_CURR_DIR)
    from prompt_diverse import PROMPT_BUILDERS, select_distractors_prompt
    from all_object import ATTR_KB, CONTAINER_KB, DISTRACTOR_KB

# ---------------- LLM bridge (local backend via code_gen/gpt_agent) ----------------
from openai import OpenAI
def gpt_agent(messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
    # OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "http://localhost:8000/v1")
    # OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "EMPTY")
    # MODEL = os.environ.get("LOCAL_LLM_MODEL", "/home/wangzhuoran/data0/MODELS/Qwen/Qwen3-8B")

    MODEL = os.environ.get("OPENAI_API_BASE", "gpt-5-mini")
    OPENAI_API_BASE = os.environ.get("OPENAI_API_KEY", "https://chatapi.onechats.ai/v1")
    OPENAI_API_KEY = "sk-Eve6SR1Tr2zZ0IhiJE8G14MzVpyun4rhbNfi49ast5ufyl5G"
    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=False,
        temperature=temperature,
    )
    return resp.choices[0].message.content

# def gpt_agent(messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
#     from zai import ZhipuAiClient
#     API_KEY = os.environ.get("OPENAI_API_KEY", "a540dedc345f7f25a6e5443cf533cc11.P1UxjgNxul3PEP0d")
#     MODEL = "glm-4.6"

#     # client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
#     client = ZhipuAiClient(api_key=API_KEY)
#     resp = client.chat.completions.create(
#         model=MODEL,
#         messages=messages,
#         # stream=False,
#         temperature=temperature,
#     )
#     return resp.choices[0].message.content

# ---------------- Allowed items ----------------
CONTAINERS: List[str] = [
    "plate", "tray", "wooden_box", "dustbin", "fluted_block", "shoe_box", "coaster",
]

OBJECTS: List[str] = [k for k in ATTR_KB.keys()]

# Get available distractors from DISTRACTOR_KB
DISTRACTORS: List[str] = [k for k in DISTRACTOR_KB.keys() if k not in OBJECTS]


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    if not os.path.isfile(path):
        return []
    out: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def collect_previous_descriptions(category: str, output_dir: str) -> List[str]:
    prev: List[str] = []
    for mode in ("correction", "wo_correction"):
        path = os.path.join(output_dir, f"{category}_{mode}.jsonl")
        for row in read_jsonl(path):
            desc = row.get("task_description")
            if isinstance(desc, dict):
                # New format: extract task text
                task_text = desc.get("task", "")
                if task_text:
                    prev.append(task_text.strip())
            elif isinstance(desc, str):
                # Old format: use as is
                prev.append(desc.strip())
    return prev


def extract_json_line(text: str) -> Optional[Dict[str, Any]]:
    text = text.strip()
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = text[start : end + 1]
        try:
            obj = json.loads(snippet)
            if isinstance(obj, dict):
                return obj
        except Exception:
            return None
    return None


def ensure_output_dir(path: str):
    os.makedirs(path, exist_ok=True)


def write_jsonl_line(path: str, obj: Dict[str, Any]):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def safe_filename(name: str) -> str:
    keep = [c if (c.isalnum() or c in ("_", "-")) else "_" for c in name]
    return "".join(keep)


def _strip_reasoning_segment(desc: str) -> str:
    parts = [p.strip() for p in desc.split('/') if p.strip()]
    kept = []
    for p in parts:
        head = p.split(':', 1)[0].strip().lower()
        if head == 'reasoning':
            continue
        kept.append(p)
    return '/'.join(kept)


def _sample_items(prev_descs: List[str]) -> Tuple[List[str], List[str], List[str]]:
    """
    Sample containers, a pool of candidate objects, and a pool of candidate distractors.
    The LLM will later select from each pool separately.

    Returns:
        (containers, object_candidates, distractor_candidates)
    """
    def usage_counts(items: List[str]) -> Dict[str, int]:
        counts = {it: 0 for it in items}
        for desc in prev_descs:
            for it in items:
                if it in desc:
                    counts[it] += 1
        return counts

    cont_counts = usage_counts(CONTAINERS)
    obj_counts = usage_counts(OBJECTS)
    distractor_counts = usage_counts(DISTRACTORS)

    # Expanded attribute buckets for greater diversity
    target_attrs_groups = [
        ["healthy", "unhealthy"],                    # nutrition contrast
        ["drinkware", "liquid_container"],           # liquid containers
        ["has_handle", "no_handle"],                 # handle presence
        ["time", "sound"],                           # time/sound utilities
        ["heavy", "light"],                          # weight contrast
        ["cleaning", "hygiene"],                     # cleaning/hygiene
        ["clothing", "footwear", "wearable"],        # wearable items
        ["dangerous", "sharp", "safe"],              # safety levels
        ["tableware", "for_eating"],                 # eating utensils
        ["primary_color", "red", "green", "blue"],   # primary colors
        ["secondary_color", "yellow", "purple"],     # secondary colors
        ["tertiary_color", "orange"],                # tertiary colors
        ["repair", "tool", "maintenance"],           # repair tools
        ["office", "electronic"],                    # office equipment
        ["food", "edible"],                          # food items
        ["toy", "entertainment"],                    # toys
        ["plant", "natural", "organic"],             # natural items
        ["metal", "wood", "plastic"],                # materials
        ["hot", "cold"],                             # temperature
        ["perishable", "durable"],                   # longevity
        ["recyclable", "disposable"],                # environmental
        ["portable", "stationary"],                  # mobility
        ["for_hot_drinks", "for_cold_drinks"],       # drink temperature
        # Additional attribute groups
        ["round", "square", "cylindrical", "rectangular", "circular"],  # shapes
        ["flat", "solid"],                           # structure
        ["sealed", "filled", "liquid"],              # container states
        ["kitchen", "cooking"],                      # kitchen items
        ["audio_input", "audio_output", "captures_sound", "produces_sound"],  # audio functionality
        ["hand_tool", "power_tool", "electric"],     # tool types
        ["fruit", "grain", "carbohydrate", "protein"],  # food types
        ["fermented", "fried", "processed", "raw"],  # food processing
        ["soft", "hard", "bouncy"],                  # texture
        ["transparent", "opaque"],                   # visibility
        ["sport", "fitness", "exercise"],            # sports/fitness
        ["reading", "educational", "knowledge"],     # educational items
        ["bath", "personal_care", "consumable"],     # personal care
        ["for_children", "for_adults"],              # age groups
        ["needs_water", "living", "decorative"],     # living things
        ["writing_tool", "stationery"],              # writing items
        ["pet_accessory", "for_animals"],            # pet items
        ["battery_powered", "power_source", "energy_storage"],  # power related
        ["fast_food", "snack"],                      # junk food
        ["nutritious", "dairy"],                     # healthy food types
        ["seasoning", "flavor_enhancer", "salty", "sweet"],  # flavors
        ["handheld", "movable"],                     # portability
        ["absorbent", "single_use"],                 # disposable items
        ["cutting_tool", "for_screws", "for_holes", "for_striking"],  # tool functions
        ["for_drinking", "for_wiping", "for_hair"],  # specific purposes
        ["computer_accessory", "for_documents", "digital"],  # tech accessories
        ["packaged", "bottle_container", "glass_container", "carton"],  # packaging types
        ["oily", "spillable"],                       # liquid properties
        ["needs_care", "requires_care", "protective"],  # care requirements
        ["strap", "adjustable"],                     # accessories
        ["small", "lightweight"],                    # size
        ["white", "black", "dark"],                  # neutral colors
        ["pink", "tint"],                            # light colors
        ["blocks", "toy_or_tool"],                   # blocks
    ]

    # Choose multiple attribute groups for diverse coverage
    num_groups = random.randint(8, 12)  # Increased to provide more diverse candidates
    chosen_groups = random.sample(target_attrs_groups, k=min(num_groups, len(target_attrs_groups)))
    chosen_attrs = set(a for g in chosen_groups for a in g)

    # Select containers (1-2)
    priority_containers = ["plate", "shoe_box", "coaster", "dustbin", "wooden_box", "tray", "fluted_block"]
    under_cont_sorted = sorted(priority_containers, key=lambda x: (cont_counts.get(x, 0), random.random()))
    k_cont = random.randint(1, 2)
    containers = under_cont_sorted[:k_cont]

    # Build SEPARATE candidate pools for objects and distractors
    # Objects pool: from OBJECTS that match chosen attributes
    object_candidates: List[str] = []
    objects_sorted = sorted(OBJECTS, key=lambda x: (obj_counts.get(x, 0), random.random()))

    for obj in objects_sorted:
        tags = set(ATTR_KB.get(obj, []))
        if tags & chosen_attrs:
            object_candidates.append(obj)

    # Ensure we have enough object candidates (6-10 items)
    target_obj_size = random.randint(6, 10)
    if len(object_candidates) < target_obj_size:
        remaining = [obj for obj in objects_sorted if obj not in object_candidates]
        additional = random.sample(remaining, min(target_obj_size - len(object_candidates), len(remaining)))
        object_candidates.extend(additional)

    random.shuffle(object_candidates)
    object_candidates = object_candidates[:target_obj_size]

    # Distractors pool: from DISTRACTORS that match chosen attributes
    distractor_candidates: List[str] = []
    distractors_sorted = sorted(DISTRACTORS, key=lambda x: (distractor_counts.get(x, 0), random.random()))

    for dist in distractors_sorted:
        tags = set(DISTRACTOR_KB.get(dist, []))
        if tags & chosen_attrs:
            distractor_candidates.append(dist)

    # Ensure we have enough distractor candidates (6-10 items)
    target_dist_size = random.randint(6, 10)
    if len(distractor_candidates) < target_dist_size:
        remaining = [dist for dist in distractors_sorted if dist not in distractor_candidates]
        additional = random.sample(remaining, min(target_dist_size - len(distractor_candidates), len(remaining)))
        distractor_candidates.extend(additional)

    random.shuffle(distractor_candidates)
    distractor_candidates = distractor_candidates[:target_dist_size]

    return containers, object_candidates, distractor_candidates


def build_task_prompt(mode: str, previous_descs: List[str]) -> Tuple[List[Dict[str, str]], List[str], List[str]]:
    """
    Build task generation prompt (Stage 1: without distractors).

    Returns:
        (messages, object_candidates, distractor_candidates)
    """
    builder = PROMPT_BUILDERS.get(("common_sense", mode))
    if builder is None:
        raise ValueError(f"Unsupported mode: {mode}")
    containers, object_candidates, distractor_candidates = _sample_items(previous_descs)
    messages = builder(previous_descs, containers, object_candidates)
    return messages, object_candidates, distractor_candidates


def select_distractors_with_llm(task_description: Dict[str, Any], distractor_candidates: List[str],
                                temperature: float = 0.0,
                                previous_distractors: Optional[List[str]] = None,
                                validation_error: Optional[str] = None) -> List[str]:
    """
    Stage 2: Use LLM to select distractors that are irrelevant to the generated task.

    Args:
        task_description: The task_description dict from stage 1
        distractor_candidates: List of candidate distractors
        temperature: LLM temperature
        previous_distractors: Previously selected distractors that failed validation (optional)
        validation_error: The validation error message (optional)

    Returns:
        List of selected distractor names
    """
    messages = select_distractors_prompt(task_description, distractor_candidates,
                                        previous_distractors, validation_error)

    try:
        response = gpt_agent(messages, temperature=temperature)
        result = extract_json_line(response)

        if result and "distractors" in result:
            selected = result["distractors"]
            # Get all available distractors (from DISTRACTOR_KB, excluding task objects)
            objects = task_description.get("scene", {}).get("objects", [])
            all_available = [k for k in DISTRACTOR_KB.keys() if k not in objects]
            # Validate that all selected items are available
            valid_distractors = [d for d in selected if d in all_available]
            # Ensure we have 3-6 distractors
            # if len(valid_distractors) < 3:
            #     # Fallback: randomly select from available distractors
            #     return random.sample(all_available, min(random.randint(3, 6), len(all_available)))
            return valid_distractors # Cap at 6
        else:
            # Fallback: randomly select
            objects = task_description.get("scene", {}).get("objects", [])
            all_available = [k for k in DISTRACTOR_KB.keys() if k not in objects]
            return random.sample(all_available, min(random.randint(3, 6), len(all_available)))
    except Exception as e:
        print(f"  [Distractor Selection] Exception: {e}, using random selection")
        objects = task_description.get("scene", {}).get("objects", [])
        all_available = [k for k in DISTRACTOR_KB.keys() if k not in objects]
        return random.sample(all_available, min(random.randint(3, 6), len(all_available)))


def is_duplicate(desc: str, prev_set: set) -> bool:
    # For new format, extract task description text
    if isinstance(desc, dict):
        task_desc = desc.get("task_description", {})
        if isinstance(task_desc, dict):
            key = task_desc.get("task", "").strip()
        else:
            key = str(task_desc).strip()
    else:
        key = str(desc).strip()
    return key in prev_set


def validate_task_logic(task_obj: Dict[str, Any], temperature: float = 0.0) -> Tuple[bool, str]:
    """
    Validate task logic using LLM to check for errors like:
    - Incorrect color classification (e.g., red as secondary_color)
    - Logical inconsistencies in task/action
    - Distractors being related to task

    Returns:
        (is_valid, error_message)
    """
    task_desc_obj = task_obj.get("task_description", {})
    if isinstance(task_desc_obj, dict):
        # New format: format as string for validation
        scene = task_desc_obj.get("scene", {})
        task_text = task_desc_obj.get("task", "")
        actions = task_desc_obj.get("action", [])

        containers = scene.get("containers", [])
        objects = scene.get("objects", [])
        distractors = scene.get("distractor", [])

        task_desc = (
            f"Containers: {', '.join(containers)}. "
            f"Objects: {', '.join(objects)}. "
            f"Distractors: {', '.join(distractors)}. "
            f"Task: {task_text}. "
            f"Actions: {' '.join(actions)}"
        )
    else:
        # Old format
        task_desc = str(task_desc_obj)

    validation_prompt = f"""You are a task validation expert. Check if this robot task contains logical errors.

Task to validate:
{task_desc}

Common error types to check:
IMPORTANT NOTES:    
0. The distractors should NOT be related to the task objects.
    - for example, the task is task: Organize electronic devices into the fluted_block and non-electronic items into the wooden_box. The distractors can be categorized as "non-electronic items". So it's not a valid task.
    - Distractors should be irrelevant to any potential task involving the selected objects.

1. Color classification errors:
   - DO NOT classify red/green/blue as secondary colors
   - DO NOT classify secondary colors (yellow, purple) as primary colors

2. Attribute mismatches:
   - Check if objects are correctly categorized, not include the correction steps
   - Verify task instructions match the actions 
   - For example, the knife is dangerous but it is categorized as safe or toy, which is incorrect.

3. Action consistency:
   - Verify actions match the task requirements
   - Check if corrections are valid (for correction mode)

Return your response in JSON format:
{{"is_valid": true/false, "error": "description of error or empty string if valid"}}

Only respond with the JSON object, no additional text."""

    messages = [
        {"role": "system", "content": "You are a precise task validation assistant. Only output valid JSON."},
        {"role": "user", "content": validation_prompt}
    ]

    try:
        response = gpt_agent(messages, temperature=temperature)
        result = extract_json_line(response)

        if result and "is_valid" in result:
            is_valid = result.get("is_valid", False)
            error = result.get("error", "Unknown validation error")
            return (is_valid, error)
        else:
            # If can't parse validation response, assume invalid to be safe
            return (False, "Failed to parse validation response")
    except Exception as e:
        print(f"  [Validation] Exception during validation: {e}")
        return (False, f"Validation exception: {e}")


def main():
    parser = argparse.ArgumentParser(description="生成更具多样性与复杂常识推理的 common_sense 任务，接口与 generate_task_info.py 相同。")
    parser.add_argument("--categories", type=str, default="common_sense", help="固定为 common_sense")
    parser.add_argument("--num_per_mode", type=int, default=5, help="每个类别每个模式生成数量")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--output_dir", type=str, default="code_gen/task_info")
    parser.add_argument("--file_mode", type=str, choices=["category", "task"], default="category",
                        help="category：按类别-模式写入单个 JSONL；task：为每条任务新建文件")
    parser.add_argument("--modes", type=str, default="correction,wo_correction",
                        help="逗号分隔模式：correction,wo_correction 之一或两者")
    parser.add_argument("--max_retries", type=int, default=4, help="生成重复时的最大重试次数")
    parser.add_argument("--truncate", action="store_true", help="在生成前清空输出文件（不保留上下文）")
    parser.add_argument("--enable_validation", action="store_true", help="启用LLM任务逻辑验证（会增加API调用）")
    args = parser.parse_args()

    ensure_output_dir(args.output_dir)
    categories = ["common_sense"]
    modes = [m.strip() for m in args.modes.split(",") if m.strip() in ("correction", "wo_correction")]
    if not modes:
        raise ValueError("--modes must include 'correction' and/or 'wo_correction'")

    for cat in categories:
        previous_all = collect_previous_descriptions(cat, args.output_dir)
        prev_set = set([p.strip() for p in previous_all])

        for mode in modes:
            out_path = os.path.join(args.output_dir, f"{cat}_{mode}.jsonl")
            if args.file_mode == "category" and args.truncate:
                open(out_path, "w").close()

            # Provide recent descriptions to the prompt for diversity guidance
            previous_mode_descs: List[str] = previous_all[-20:]  # limited context for variety without overfitting

            success_count = 0
            attempt_count = 0
            max_attempts = args.num_per_mode * (args.max_retries + 2)  # Allow more attempts to reach target

            while success_count < args.num_per_mode and attempt_count < max_attempts:
                attempt_count += 1
                retries = 0
                obj: Optional[Dict[str, Any]] = None

                while retries <= args.max_retries:
                    # ========== STAGE 1: Generate task (without distractors) ==========
                    msgs, object_candidates, distractor_candidates = build_task_prompt(mode, previous_mode_descs)
                    try:
                        out = gpt_agent(msgs, temperature=args.temperature)
                    except Exception as e:
                        print(f"  [Attempt {attempt_count}] Stage 1 generation error: {e}, skipping...")
                        break  # Skip this attempt, don't write to file

                    cand = extract_json_line(out)
                    if cand is None:
                        print(f"  [Attempt {attempt_count}] Failed to parse JSON, retrying...")
                        retries += 1
                        continue

                    # Validate new JSON structure
                    if "task_description" not in cand:
                        print(f"  [Attempt {attempt_count}] Missing task_description, retrying...")
                        retries += 1
                        continue
                    print(cand)
                    task_desc = cand.get("task_description")
                    if not isinstance(task_desc, dict):
                        print(f"  [Attempt {attempt_count}] task_description should be dict, retrying...")
                        retries += 1
                        continue

                    if "scene" not in task_desc or "task" not in task_desc or "action" not in task_desc:
                        print(f"  [Attempt {attempt_count}] Missing required fields in task_description, retrying...")
                        retries += 1
                        continue

                    scene = task_desc.get("scene", {})
                    if "containers" not in scene or "objects" not in scene:
                        print(f"  [Attempt {attempt_count}] Missing containers or objects in scene, retrying...")
                        retries += 1
                        continue

                    # Check for duplicates (using task text)
                    task_text = task_desc.get("task", "")
                    if is_duplicate(cand, prev_set):
                        print(f"  [Attempt {attempt_count}] Duplicate task detected, retrying...")
                        retries += 1
                        continue

                    # ========== STAGE 2: Select distractors with iterative validation ==========
                    print(f"  [Attempt {attempt_count}] Stage 1 passed, selecting distractors...")

                    # Filter out objects that were already selected in stage 1
                    selected_objects = scene.get("objects", [])
                    filtered_distractor_candidates = [d for d in distractor_candidates if d not in selected_objects]

                    if len(filtered_distractor_candidates) < 3:
                        print(f"  [Attempt {attempt_count}] Not enough distractor candidates after filtering, retrying...")
                        retries += 1
                        continue

                    # Iterative distractor selection and validation
                    max_distractor_retries = 2  # Maximum retries for distractor selection
                    distractor_retry = 0
                    distractors = None
                    previous_distractors = None
                    validation_error = None

                    while distractor_retry < max_distractor_retries:
                        try:
                            # Select distractors (with previous failure info if available)
                            distractors = select_distractors_with_llm(
                                task_desc,
                                filtered_distractor_candidates,
                                temperature=0.0,
                                previous_distractors=previous_distractors,
                                validation_error=validation_error
                            )
                            print(f"  [Attempt {attempt_count}][Distractor retry {distractor_retry+1}] Selected {len(distractors)} distractors: {', '.join(distractors)}")
                        except Exception as e:
                            print(f"  [Attempt {attempt_count}][Distractor retry {distractor_retry+1}] Selection error: {e}")
                            distractor_retry += 1
                            continue

                        # Add distractors to scene for validation
                        scene["distractor"] = distractors
                        task_desc["scene"] = scene
                        cand["task_description"] = task_desc

                        # Validate task logic (if enabled)
                        if args.enable_validation:
                            print(f"  [Attempt {attempt_count}][Distractor retry {distractor_retry+1}] Validating task logic...")
                            is_valid, error_msg = validate_task_logic(cand, temperature=0.0)

                            if not is_valid:
                                print(f"  [Attempt {attempt_count}][Distractor retry {distractor_retry+1}] Validation failed: {error_msg}")
                                # Store failed distractors and error for next iteration
                                previous_distractors = distractors
                                validation_error = error_msg
                                distractor_retry += 1
                                continue
                            else:
                                print(f"  [Attempt {attempt_count}][Distractor retry {distractor_retry+1}] Validation passed!")
                                break
                        else:
                            # No validation enabled, accept distractors
                            break

                    # Check if we succeeded in finding valid distractors
                    if distractor_retry >= max_distractor_retries:
                        print(f"  [Attempt {attempt_count}] Failed to find valid distractors after {max_distractor_retries} retries, retrying entire task...")
                        retries += 1
                        continue

                    # Add sequence number to task name
                    original_task_name = cand.get("task_name", f"{cat}_{mode}_auto_{success_count}")
                    if re.match(r'^\d+_', original_task_name):
                        original_task_name = re.sub(r'^\d+_', '', original_task_name)
                    cand["task_name"] = f"{success_count + 1}_{original_task_name}"

                    obj = cand
                    break

                # Only write if successful
                if obj is not None:
                    if args.file_mode == "category":
                        write_jsonl_line(out_path, obj)
                    else:
                        task_file = os.path.join(args.output_dir, f"{safe_filename(obj['task_name'])}.jsonl")
                        with open(task_file, "w", encoding="utf-8") as f:
                            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

                    # Update prev_set with task text (for duplicate checking)
                    task_desc = obj.get("task_description", {})
                    if isinstance(task_desc, dict):
                        task_text = task_desc.get("task", "")
                        prev_set.add(task_text.strip())
                        previous_all.append(task_text.strip())
                    previous_mode_descs = previous_all[-20:]
                    success_count += 1
                    print(f"  [Success {success_count}/{args.num_per_mode}] Generated: {obj['task_name']}")

            print(f"Generated {success_count}/{args.num_per_mode} tasks for 'common_sense' [{mode}] -> {out_path if args.file_mode=='category' else args.output_dir}")


if __name__ == "__main__":
    main()
