import os
import json
import argparse
import random
import re
from typing import Dict, Any, List, Optional, Tuple
import sys

try:
    # When executed as a module: python -m script.auto_gen.generate_task_info_diverse
    from .prompt_diverse import PROMPT_BUILDERS, ATTR_KB
except Exception:
    # When executed as a script: python script/auto_gen/generate_task_info_diverse.py
    _CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    if _CURR_DIR not in sys.path:
        sys.path.append(_CURR_DIR)
    from prompt_diverse import PROMPT_BUILDERS, ATTR_KB

# ---------------- LLM bridge (local backend via code_gen/gpt_agent) ----------------
# from openai import OpenAI
# def gpt_agent(messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
#     OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "http://localhost:8000/v1")
#     OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "EMPTY")
#     MODEL = os.environ.get("LOCAL_LLM_MODEL", "/home/wangzhuoran/data0/MODELS/Qwen/Qwen3-8B")

#     client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
#     resp = client.chat.completions.create(
#         model=MODEL,
#         messages=messages,
#         stream=False,
#         temperature=temperature,
#     )
#     return resp.choices[0].message.content

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

# ---------------- Allowed items ----------------
CONTAINERS: List[str] = [
    "plate", "tray", "wooden_box", "dustbin", "fluted_block", "shoe_box", "coaster",
]

OBJECTS: List[str] = [
    "hammer", "microphone", "bottle", "can", "cup", "cup_with_handle", "cup_without_handle", "pot-with-plant",
    "apple", "hamburg", "bread", "french_fries", "toycar", "tissue-box", "scanner", "drill", "screwdriver", "fork",
    "knife", "mug", "shoe", "book", "sand-clock", "alarm-clock", "mouse", "stapler", "shampoo", "bell", "dumbbell", "teanet",
    "red_block", "blue_block", "green_block", "yellow_block", "purple_block", "orange_block", "pink_block",
]


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
            if isinstance(desc, str):
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


def _sample_items(prev_descs: List[str]) -> Tuple[List[str], List[str]]:
    # Prioritize underused items AND ensure diverse attribute coverage
    def usage_counts(items: List[str]) -> Dict[str, int]:
        counts = {it: 0 for it in items}
        for desc in prev_descs:
            for it in items:
                if it in desc:
                    counts[it] += 1
        return counts

    cont_counts = usage_counts(CONTAINERS)
    obj_counts = usage_counts(OBJECTS)

    # Underused ranking
    under_cont = sorted(CONTAINERS, key=lambda x: (cont_counts.get(x, 0), random.random()))
    under_obj = sorted(OBJECTS, key=lambda x: (obj_counts.get(x, 0), random.random()))

    # Expanded attribute buckets for greater diversity
    target_attrs_groups = [
        ["healthy", "unhealthy"],                    # nutrition contrast
        ["drinkware", "liquid_container"],           # liquid containers
        ["has_handle", "no_handle"],                 # handle presence
        ["time", "sound"],                           # time/sound utilities
        ["heavy", "light"],                          # weight contrast
        ["cleaning", "hygiene"],                     # cleaning/hygiene
        ["clothing", "footwear"],                    # wearable items
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
    ]

    # Choose a larger subset for more diverse coverage (increased from 5 to 6-8)
    num_groups = random.randint(6, 8)
    chosen_groups = random.sample(target_attrs_groups, k=min(num_groups, len(target_attrs_groups)))
    chosen_attrs = set(a for g in chosen_groups for a in g)

    # Containers: ensure at least one that aligns with rules (plate, shoe_box, coaster, dustbin, wooden_box)
    priority_containers = ["plate", "shoe_box", "coaster", "dustbin", "wooden_box", "tray", "fluted_block"]
    under_cont_sorted = sorted(priority_containers, key=lambda x: (cont_counts.get(x, 0), random.random()))
    k_cont = random.randint(1, 2)  # 1-2 containers
    containers = under_cont_sorted[:k_cont]

    # Calculate max objects to ensure total (containers + objects) <= 7
    max_objects = 7 - k_cont  # Maximum objects allowed
    k_total = random.randint(max(2, max_objects - 2), max_objects)  # 2-5 objects typically

    # Pick objects that collectively cover chosen attributes, preferring underused
    selected: List[str] = []
    covered: set = set()
    for obj in under_obj:
        tags = set(ATTR_KB.get(obj, []))
        if tags & chosen_attrs:
            selected.append(obj)
            covered |= (tags & chosen_attrs)
        if len(selected) >= k_total:
            break

    # Backfill with more underused/random objects if needed
    for obj in under_obj:
        if len(selected) >= k_total:
            break
        if obj not in selected:
            selected.append(obj)
    while len(selected) < k_total:
        cand = random.choice(OBJECTS)
        if cand not in selected:
            selected.append(cand)

    random.shuffle(selected)

    # Ensure total doesn't exceed 7
    total_items = len(containers) + len(selected)
    if total_items > 7:
        selected = selected[:7 - len(containers)]

    return containers, selected


def build_task_prompt(mode: str, previous_descs: List[str]) -> List[Dict[str, str]]:
    builder = PROMPT_BUILDERS.get(("common_sense", mode))
    if builder is None:
        raise ValueError(f"Unsupported mode: {mode}")
    containers, objects = _sample_items(previous_descs)
    return builder(previous_descs, containers, objects)


def is_duplicate(desc: str, prev_set: set) -> bool:
    key = desc.strip()
    return key in prev_set


def validate_task_logic(task_obj: Dict[str, Any], temperature: float = 0.0) -> Tuple[bool, str]:
    """
    Validate task logic using LLM to check for errors like:
    - Incorrect color classification (e.g., red as secondary_color)
    - Logical inconsistencies in task/action

    Returns:
        (is_valid, error_message)
    """
    task_desc = task_obj.get("task_description", "")

    validation_prompt = f"""You are a task validation expert. Check if this robot task contains logical errors.

Task to validate:
{task_desc}

Common error types to check:
1. Color classification errors:
   - Primary colors (RGB): red, green, blue
   - Secondary colors: yellow, purple (magenta), cyan
   - Tertiary colors: orange
   - DO NOT classify red/green/blue as secondary colors

2. Attribute mismatches:
   - Check if objects are correctly categorized (healthy/unhealthy, has_handle/no_handle, etc.)
   - Verify task instructions match the actions taken

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
                    msgs = build_task_prompt(mode, previous_mode_descs)
                    try:
                        out = gpt_agent(msgs, temperature=args.temperature)
                    except Exception as e:
                        print(f"  [Attempt {attempt_count}] Generation error: {e}, skipping...")
                        break  # Skip this attempt, don't write to file

                    cand = extract_json_line(out)
                    if cand is None:
                        print(f"  [Attempt {attempt_count}] Failed to parse JSON, retrying...")
                        retries += 1
                        continue

                    # Add sequence number to task name
                    original_task_name = cand.get("task_name", f"{cat}_{mode}_auto_{success_count}")
                    # Remove old numbering if exists
                    if re.match(r'^\d+_', original_task_name):
                        original_task_name = re.sub(r'^\d+_', '', original_task_name)
                    # Add new sequence number (1-indexed)
                    cand["task_name"] = f"{success_count + 1}_{original_task_name}"

                    if "task_description" not in cand:
                        print(f"  [Attempt {attempt_count}] Missing task_description, retrying...")
                        retries += 1
                        continue

                    cand["task_description"] = _strip_reasoning_segment(cand.get("task_description", "").strip())
                    desc = cand["task_description"].strip()

                    # diversity check: must change phrasing and rules
                    # Encourage category-driven language (avoid many direct item names in 'task:')
                    task_part = next((seg for seg in desc.split('/') if seg.lower().startswith('task:')), '')
                    # Use word boundary to avoid substring matches (e.g., "cup" shouldn't match "cup_with_handle")
                    all_items = OBJECTS + CONTAINERS
                    # Sort by length (longest first) to avoid substring issues
                    all_items_sorted = sorted(all_items, key=len, reverse=True)
                    name_count = 0
                    for name in all_items_sorted:
                        # Use word boundaries to match complete words
                        if re.search(r'\b' + re.escape(name.replace('_', '[ _-]')) + r'\b', task_part, re.IGNORECASE):
                            name_count += 1

                    # Allow up to 3 explicit names in task (relaxed constraint)
                    if name_count > 3:
                        print(f"  [Attempt {attempt_count}] Too many explicit names in task ({name_count}), retrying...")
                        retries += 1
                        continue

                    # Check for duplicates
                    if is_duplicate(desc, prev_set):
                        print(f"  [Attempt {attempt_count}] Duplicate task detected, retrying...")
                        retries += 1
                        continue

                    # Validate task logic using LLM (if enabled)
                    if args.enable_validation:
                        print(f"  [Attempt {attempt_count}] Validating task logic...")
                        is_valid, error_msg = validate_task_logic(cand, temperature=0.0)

                        if not is_valid:
                            print(f"  [Attempt {attempt_count}] Validation failed: {error_msg}, retrying...")
                            retries += 1
                            continue

                        print(f"  [Attempt {attempt_count}] Validation passed!")

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

                    prev_set.add(obj["task_description"].strip())
                    previous_all.append(obj["task_description"].strip())
                    previous_mode_descs = previous_all[-20:]
                    success_count += 1
                    print(f"  [Success {success_count}/{args.num_per_mode}] Generated: {obj['task_name']}")

            print(f"Generated {success_count}/{args.num_per_mode} tasks for 'common_sense' [{mode}] -> {out_path if args.file_mode=='category' else args.output_dir}")


if __name__ == "__main__":
    main()
