import os
import json
import argparse
from typing import Any, Dict, List, Optional, Tuple


# =================== LLM bridge (uses local backend) ===================
def gpt_agent(messages: List[Dict[str, str]], temperature: float = 0.0) -> str:
    from code_gen.gpt_agent import generate
    return generate(messages, gpt="local", temperature=temperature)


# =========================== Episode utilities =========================
def subplan_dir(task_name: str, task_config: str) -> str:
    return os.path.join("data", task_name, task_config, "sub_plan")


def load_scene_info(task_name: str, task_config: str) -> Optional[Dict[str, Any]]:
    p = os.path.join("data", task_name, task_config, "scene_info.json")
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def list_episode_ids(sp_dir: str) -> List[int]:
    ids: List[int] = []
    if not os.path.isdir(sp_dir):
        return ids
    for fn in os.listdir(sp_dir):
        if fn.startswith("episode") and fn.endswith(".json"):
            try:
                ids.append(int(fn[len("episode"): -len(".json")]))
            except Exception:
                pass
    return sorted(ids)


def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, obj: Any):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def load_points(task_name: str, task_config: str, episode_id: int) -> Optional[List[Dict[str, Any]]]:
    epi_dir = os.path.join("robotwin_data", task_name, task_config, f"episode{episode_id}")
    p = os.path.join(epi_dir, "points.json")
    if not os.path.exists(p):
        return None
    return read_json(p)


def points_by_frame(points_doc: Optional[List[Dict[str, Any]]]) -> Dict[int, List[Dict[str, Any]]]:
    byf: Dict[int, List[Dict[str, Any]]] = {}
    if not points_doc:
        return byf
    for entry in points_doc:
        frame = int(entry.get("frame_idx", 0))
        byf.setdefault(frame, []).extend(entry.get("targets", []))
    return byf


# =========================== Prompt generators =========================
BASE_REASONING_CATEGORIES: Dict[str, str] = {
    "common_sense": "Leverage everyday commonsense about objects and goals.",
    "counting": "Consider quantities, presence/absence and selection by count.",
    "spatial": "Use spatial relations (left/right/front/behind/inside/near).",
    # Extra categories
    "temporal": "Consider order, preconditions and time-dependent dependencies.",
    "physics": "Use physical intuition (stability, gravity, collisions, balance).",
    "affordance": "Use object affordances and typical uses to guide choices.",
    "causality": "Reason about causes and effects between actions and outcomes.",
    "constraint": "Apply explicit constraints (safety, rules, forbidden zones).",
    "intention": "Infer intended goal or user preference from context.",
    "planning": "Structure multi-step plans, subgoals, and decomposition.",
}


def build_task_info_prompt(context: Dict[str, Any]) -> List[Dict[str, str]]:
    system = (
        "You are an expert data annotator.\n"
        "Produce a compact JSON called task_info with keys: \n"
        "- goal (string)\n- objects (list of strings)\n- constraints (list)\n- env (dict)\n- success_criteria (list)\n"
        "Do not add comments or extra text; output only valid JSON."
    )
    user = (
        "Summarize the task context into task_info JSON. Use only given info.\n\n"
        f"context:\n{json.dumps(context, ensure_ascii=False, indent=2)}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def build_reasoning_prompt(
    category: str,
    with_correction: bool,
    task_info: Dict[str, Any],
    subplan_step: Dict[str, Any],
    candidates: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, str]]:
    cat_hint = BASE_REASONING_CATEGORIES.get(category, "Provide concise, relevant reasoning.")
    corr_hint = (
        "If there are likely mistakes or ambiguities, briefly point them out and propose a fix before the final action.\n"
        if with_correction
        else "Do not include any correction or critique content.\n"
    )
    system = (
        "You are an expert robot planner.\n"
        f"Reasoning style: {cat_hint}\n"
        f"{corr_hint}"
        "Then output exactly one final action on the last line wrapped in <action>...</action>.\n"
        "Allowed actions:\n1. pick(target, point)\n2. place(container, point)\n3. done()\n"
        "If a pixel point is given for the relevant target/container, use it verbatim."
    )

    cand_text = ""
    if candidates:
        light = [{"name": c.get("target_name"), "pixel": c.get("pixel")} for c in candidates]
        cand_text = f"\n\nCandidate points:\n{json.dumps(light, ensure_ascii=False)}"

    user = (
        f"task_info:\n{json.dumps(task_info, ensure_ascii=False, indent=2)}\n\n"
        f"subplan_step:\n{json.dumps(subplan_step, ensure_ascii=False, indent=2)}\n"
        f"{cand_text}\n\n"
        "Provide brief reasoning first, then the last line must be <action>...</action>."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


# =============================== Pipeline ===============================
def batch_generate(
    task_name: str,
    task_config: str,
    categories: List[str],
    with_correction: List[bool],
    only_episode: Optional[int] = None,
    temperature: float = 0.0,
):
    sp_dir = subplan_dir(task_name, task_config)
    scene = load_scene_info(task_name, task_config) or {}
    eps = [only_episode] if only_episode is not None else list_episode_ids(sp_dir)

    for eid in eps:
        subplan_path = os.path.join(sp_dir, f"episode{eid}.json")
        if not os.path.exists(subplan_path):
            print(f"Skip episode {eid}: missing subplan {subplan_path}")
            continue
        subplan = read_json(subplan_path)

        # 1) Generate task_info for this episode using scene + a light view of subplan header
        context = {
            "scene_info": scene,
            "subplan_meta": [{"frame_idx": s.get("frame_idx"), "action": s.get("action"), "targets": s.get("target_name")} for s in subplan],
        }
        instr_msgs = build_task_info_prompt(context)
        task_info_text = gpt_agent(instr_msgs, temperature=temperature)
        try:
            task_info = json.loads(task_info_text)
        except Exception:
            task_info = {"raw": task_info_text}

        epi_dir = os.path.join("robotwin_data", task_name, task_config, f"episode{eid}")
        write_json(os.path.join(epi_dir, "task_info.json"), task_info)

        # 2) Load candidate points if exist
        pts_doc = load_points(task_name, task_config, eid)
        by_frame = points_by_frame(pts_doc)

        # 3) For each category and correction mode, generate reasoning per step
        for cat in categories:
            for corr in with_correction:
                outputs: List[Dict[str, Any]] = []
                for step in subplan:
                    frame = int(step.get("frame_idx", 0))
                    cands = by_frame.get(frame, [])
                    msgs = build_reasoning_prompt(cat, corr, task_info, step, cands)
                    try:
                        txt = gpt_agent(msgs, temperature=temperature)
                    except Exception as e:
                        txt = f"<REASONING_FAILED: {e}>\n<action>done()</action>"
                    outputs.append({"frame_idx": frame, "category": cat, "with_correction": corr, "output": txt})

                suffix = f"{cat}{'_corr' if corr else ''}.json"
                outpath = os.path.join(epi_dir, f"reasoning_{suffix}")
                write_json(outpath, {"steps": outputs})
                print(f"episode {eid}: wrote {outpath}")


def main():
    parser = argparse.ArgumentParser(description="Batch-generate task_info and category-specific reasoning prompts via LLM")
    parser.add_argument("task_name", type=str)
    parser.add_argument("task_config", type=str)
    parser.add_argument("--categories", type=str, default="common_sense,counting,spatial,temporal,physics,affordance,causality,constraint,intention,planning")
    parser.add_argument("--with_correction", type=str, default="false,true", help="comma list of booleans")
    parser.add_argument("--only_episode", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=0.0)
    args = parser.parse_args()

    cats = [c.strip() for c in args.categories.split(",") if c.strip()]
    corrs = []
    for s in args.with_correction.split(","):
        s = s.strip().lower()
        corrs.append(s in ("true", "1", "yes", "y"))

    batch_generate(
        task_name=args.task_name,
        task_config=args.task_config,
        categories=cats,
        with_correction=corrs,
        only_episode=args.only_episode,
        temperature=args.temperature,
    )


if __name__ == "__main__":
    main()

