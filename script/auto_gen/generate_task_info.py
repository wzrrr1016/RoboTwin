import os
import json
import argparse
from typing import Dict, Any, List, Optional, Tuple
import sys
import os
try:
    # When executed as a module: python -m script.auto_gen.generate_task_info
    from .prompts import PROMPT_BUILDERS
except Exception:
    # When executed as a script: python script/auto_gen/generate_task_info.py
    _CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    if _CURR_DIR not in sys.path:
        sys.path.append(_CURR_DIR)
    from prompts import PROMPT_BUILDERS

# ---------------- LLM bridge (local backend via code_gen/gpt_agent) ----------------
from openai import OpenAI


def gpt_agent(messages: List[Dict[str, str]], temperature: float = 0.0) -> str:
    OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "http://localhost:8000/v1")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "EMPTY")
    MODEL = os.environ.get("LOCAL_LLM_MODEL", "/home/wangzhuoran/data0/MODELS/Qwen/Qwen3-8B")

    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=False,
        temperature=temperature,
    )
    return resp.choices[0].message.content


# ---------------- Category hints and allowed objects ----------------
CATEGORY_HINTS: Dict[str, str] = {
    "common_sense": "根据日常常识进行分类与放置（如食物与工具的区分）",
    "counting": "按数量与颜色进行选择与放置（精确计数）",
    "spatial": "依据空间关系安排物体（左/右/内/上/附近等）",
}

AVAILABLE_OBJECTS: List[str] = [
    # containers
    "bowl", "plate", "tray", "wooden_box", "dustbin", "fluted_block", "shoe_box","coaster"
    # objects
    "hammer", "microphone", "bottle", "can", "cup", "cup_with_handle", "cup_without_handle", "pot-with-plant",
    "apple", "hamburg", "bread", "french_fries", "toycar","tissue-box","scanner","drill","screwdriver","fork",
    "knife","mug","shoe","book","sand-clock","alarm-clock","mouse","stapler","shampoo","bell","dumbbell","teanet",
    
    # color blocks
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


def build_task_prompt(category: str, mode: str, previous_descs: List[str]) -> List[Dict[str, str]]:
    builder = PROMPT_BUILDERS.get((category, mode))
    if builder is None:
        raise ValueError(f"Unsupported category/mode: {category}/{mode}")
    return builder(previous_descs, AVAILABLE_OBJECTS)


def is_duplicate(desc: str, prev_set: set) -> bool:
    key = desc.strip()
    return key in prev_set


def main():
    parser = argparse.ArgumentParser(description="按类别与模式(correction/wo_correction)生成任务，包含推理段且避免重复。")
    parser.add_argument("--categories", type=str, required=True, help="逗号分隔类别：common_sense,counting,spatial")
    parser.add_argument("--num_per_mode", type=int, default=5, help="每个类别每个模式生成数量")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--output_dir", type=str, default="code_gen/task_info")
    parser.add_argument("--file_mode", type=str, choices=["category", "task"], default="category",
                        help="category：按类别-模式写入单个 JSONL；task：为每条任务新建文件")
    parser.add_argument("--modes", type=str, default="correction,wo_correction",
                        help="逗号分隔模式：correction,wo_correction 之一或两者")
    parser.add_argument("--max_retries", type=int, default=3, help="生成重复时的最大重试次数")
    parser.add_argument("--truncate", action="store_true", help="在生成前清空输出文件（不保留上下文）")
    args = parser.parse_args()

    ensure_output_dir(args.output_dir)
    categories = [c.strip() for c in args.categories.split(",") if c.strip()]
    modes = [m.strip() for m in args.modes.split(",") if m.strip() in ("correction", "wo_correction")]
    if not modes:
        raise ValueError("--modes must include 'correction' and/or 'wo_correction'")

    for cat in categories:
        # Load context across both modes to avoid duplicates within the category
        previous_all = collect_previous_descriptions(cat, args.output_dir)
        prev_set = set([p.strip() for p in previous_all])

        for mode in modes:
            out_path = os.path.join(args.output_dir, f"{cat}_{mode}.jsonl")
            if args.file_mode == "category" and args.truncate:
                open(out_path, "w").close()

            # Refresh per-mode previous for context (after possible truncate)
            previous_mode_descs = collect_previous_descriptions(cat, args.output_dir)

            for i in range(args.num_per_mode):
                retries = 0
                obj: Optional[Dict[str, Any]] = None
                while retries <= args.max_retries:
                    msgs = build_task_prompt(cat, mode, previous_mode_descs)
                    try:
                        out = gpt_agent(msgs, temperature=args.temperature)
                    except Exception as e:
                        obj = {
                            "task_name": f"{cat}_{mode}_gen_error_{i}",
                            "task_description": f"scene: n/a/reasoning: {cat}/task: generation failed ({e})/action: n/a",
                        }
                        break

                    cand = extract_json_line(out) or {
                        "task_name": f"{cat}_{mode}_fallback_{i}",
                        "task_description": "scene: fallback/reasoning: {cat}/task: fallback/action: fallback",
                    }

                    # Normalize
                    if "task_name" not in cand:
                        cand["task_name"] = f"{cat}_{mode}_auto_{i}"
                    if "task_description" not in cand:
                        cand["task_description"] = f"scene: .../reasoning: {cat}/task: .../action: ..."

                    desc = cand["task_description"].strip()

                    # Enforce duplication check
                    if not is_duplicate(desc, prev_set):
                        obj = cand
                        break
                    else:
                        retries += 1
                # Write result
                if obj is None:
                    obj = {
                        "task_name": f"{cat}_{mode}_dup_exhausted_{i}",
                        "task_description": f"scene: placeholder/reasoning: {cat}/task: failed to produce unique/action: placeholder",
                    }

                if args.file_mode == "category":
                    write_jsonl_line(out_path, obj)
                else:
                    task_file = os.path.join(args.output_dir, f"{safe_filename(obj['task_name'])}.jsonl")
                    with open(task_file, "w", encoding="utf-8") as f:
                        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

                # Update context sets
                prev_set.add(obj["task_description"].strip())
                previous_mode_descs.append(obj["task_description"].strip())

            print(f"Generated {args.num_per_mode} tasks for '{cat}' [{mode}] -> {out_path if args.file_mode=='category' else args.output_dir}")


if __name__ == "__main__":
    main()

"""
示例用法:
python script/auto_gen/generate_task_info.py \
    --categories common_sense,counting,spatial \
    --num_per_mode 5 \
    --temperature 0.0 \
    --output_dir code_gen/task_info \
    --file_mode category

cd 
python script/auto_gen/generate_task_info.py \
    --categories common_sense \
    --modes correction \
    --num_per_mode 5 \
    --output_dir code_gen/task_info
"""
