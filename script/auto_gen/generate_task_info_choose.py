import os
import json
import argparse
from typing import Dict, Any, List, Optional
import sys

try:
    # When executed as a module: python -m script.auto_gen.generate_task_info_choose
    from .prompt_choose import PROMPT_BUILDERS
except Exception:
    # When executed as a script: python script/auto_gen/generate_task_info_choose.py
    _CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    if _CURR_DIR not in sys.path:
        sys.path.append(_CURR_DIR)
    from prompt_choose import PROMPT_BUILDERS


def gpt_agent(messages: List[Dict[str, str]], temperature: float = 0.0) -> str:
    from zai import ZhipuAiClient
    API_KEY = os.environ.get("OPENAI_API_KEY", "a540dedc345f7f25a6e5443cf533cc11.P1UxjgNxul3PEP0d")
    MODEL = "glm-4-flash"

    client = ZhipuAiClient(api_key=API_KEY)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content


# Available items (full lists provided to the model to choose from)
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


def build_task_prompt(mode: str) -> List[Dict[str, str]]:
    builder = PROMPT_BUILDERS.get(("common_sense", mode))
    if builder is None:
        raise ValueError(f"Unsupported mode: {mode}")
    # Provide full lists; the model chooses 1–2 containers and 4–6 objects
    return builder([], CONTAINERS, OBJECTS)


def is_duplicate(desc: str, prev_set: set) -> bool:
    key = desc.strip()
    return key in prev_set


def main():
    parser = argparse.ArgumentParser(description="基于完整物品清单生成 common_sense 任务：任务描述不包含显式 reasoning 字段，但在 'task:' 中体现复杂常识推理。模型从给定清单中自行选择物品。")
    parser.add_argument("--categories", type=str, default="common_sense", help="任务类别")
    parser.add_argument("--num_per_mode", type=int, default=5, help="每个模式生成数量")
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
    category = args.categories
    modes = [m.strip() for m in args.modes.split(",") if m.strip() in ("correction", "wo_correction")]
    if not modes:
        raise ValueError("--modes must include 'correction' and/or 'wo_correction'")

    previous_all = collect_previous_descriptions(category, args.output_dir)
    prev_set = set([p.strip() for p in previous_all])

    for mode in modes:
        out_path = os.path.join(args.output_dir, f"{category}_{mode}.jsonl")
        if args.file_mode == "category" and args.truncate:
            open(out_path, "w").close()

        # No prior tasks in prompt context
        for i in range(args.num_per_mode):
            retries = 0
            obj: Optional[Dict[str, Any]] = None
            while retries <= args.max_retries:
                msgs = build_task_prompt(mode)
                try:
                    out = gpt_agent(msgs, temperature=args.temperature)
                except Exception as e:
                    obj = {
                        "task_name": f"{category}_{mode}_gen_error_{i}",
                        "task_description": f"scene: n/a/task: generation failed ({e})/action: n/a",
                    }
                    break

                cand = extract_json_line(out) or {
                    "task_name": f"{category}_{mode}_fallback_{i}",
                    "task_description": "scene: fallback/task: fallback/action: fallback",
                }

                if "task_name" not in cand:
                    cand["task_name"] = f"{category}_{mode}_auto_{i}"
                if "task_description" not in cand:
                    cand["task_description"] = f"scene: .../task: .../action: ..."

                cand["task_description"] = _strip_reasoning_segment(cand.get("task_description", "").strip())
                desc = cand["task_description"].strip()

                if not is_duplicate(desc, prev_set):
                    obj = cand
                    break
                else:
                    retries += 1

            if obj is None:
                obj = {
                    "task_name": f"{category}_{mode}_dup_exhausted_{i}",
                    "task_description": f"scene: placeholder/task: failed to produce unique/action: placeholder",
                }

            if args.file_mode == "category":
                write_jsonl_line(out_path, obj)
            else:
                task_file = os.path.join(args.output_dir, f"{safe_filename(obj['task_name'])}.jsonl")
                with open(task_file, "w", encoding="utf-8") as f:
                    f.write(json.dumps(obj, ensure_ascii=False) + "\n")

            prev_set.add(obj["task_description"].strip())

        print(f"Generated {args.num_per_mode} tasks for 'common_sense' [{mode}] -> {out_path if args.file_mode=='category' else args.output_dir}")


if __name__ == "__main__":
    main()
