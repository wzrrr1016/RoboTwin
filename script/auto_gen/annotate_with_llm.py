import os
import json
import argparse
from typing import Any, Dict, List, Optional, Tuple


# ============== Plug-in LLM Caller (replace with your gpt_agent) ==============
def gpt_agent(messages: List[Dict[str, str]], model: str = "local") -> str:
    """Use code_gen/gpt_agent.py local backend to generate text."""
    import sys, os
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    from code_gen.gpt_agent import generate
    return generate(messages, gpt="local", temperature=0)


# ============================ Prompt Builders =============================
def build_instruction_prompt_from_refs(ref_tasks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Builds chat messages to produce a single instruction for the whole dataset.

    Requirements:
    - Instruction must NOT directly describe the concrete steps/actions.
    - Instruction must NOT contain any correction/critique content.
    - Keep it concise, context-aware, and neutral.
    """
    system = (
        "You are an expert robot task instructor.\n"
        "Constraints:\n"
        "- Do not explicitly describe the concrete steps or actions.\n"
        "- Do not include any correction or critique content.\n"
        "- Keep the instruction succinct, context-aware, and neutral.\n"
        "Output only the instruction without extra commentary."
    )

    ref_compact = [{"task_name": r.get("task_name"), "task_description": r.get("task_description")} for r in ref_tasks[:8]]
    user = (
        "Based on the following reference task descriptions, synthesize one concise instruction\n"
        "that would guide the agent implicitly for similar episodes.\n\n"
        f"reference_tasks:\n{json.dumps(ref_compact, ensure_ascii=False, indent=2)}\n"
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def build_reasoning_prompt(
    ref_tasks: List[Dict[str, Any]],
    subplan_step: Dict[str, Any],
    candidate_points: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, str]]:
    """Builds chat messages to produce reasoning and a final action.

    Requirements:
    - Reason about why to take this step given subplan and task_info.
    - Choose an action from the set:\n"
    "  1. pick(target, point)\n  2. place(container, point)\n  3. done()\n"
    - The final line must be the action wrapped in <action>...</action> exactly.
    - If candidate_points are provided, pick the matching point for the relevant target/container.
    - Do not include correction/critique content.
    """
    system = (
        "You are an expert robot planner.\n"
        "Given a subplan step, provide concise reasoning (why this step is needed).\n"
        "Do not include correction or critique content.\n"
        "Final action will be auto-filled using real points; you do NOT output the action."
    )

    # Normalize candidate points (list of dicts with fields: target_name, pixel)
    cand_desc = ""
    if candidate_points:
        compact = [
            {"name": c.get("target_name"), "pixel": c.get("pixel")} for c in candidate_points
        ]
        cand_desc = f"\n\nCandidate points (if applicable):\n{json.dumps(compact, ensure_ascii=False)}"

    ref_compact = [{"task_name": r.get("task_name"), "task_description": r.get("task_description")} for r in ref_tasks[:6]]
    user = (
        "Given the reference task family and the subplan step, provide a brief reasoning for this step.\n\n"
        f"reference_tasks:\n{json.dumps(ref_compact, ensure_ascii=False, indent=2)}\n\n"
        f"subplan_step:\n{json.dumps(subplan_step, ensure_ascii=False, indent=2)}\n"
        f"{cand_desc}\n\n"
        "Only output reasoning; do NOT output the final action."
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


# =============================== I/O Helpers ===============================
def load_subplan_dir(task_name: str, task_config: str) -> str:
    return os.path.join("data", task_name, task_config, "sub_plan")


def load_points_for_episode(
    task_name: str, task_config: str, episode_id: int
) -> Optional[List[Dict[str, Any]]]:
    epi_dir = os.path.join("robotwin_data", task_name, task_config, f"episode{episode_id}")
    points_path = os.path.join(epi_dir, "points.json")
    if not os.path.exists(points_path):
        return None
    with open(points_path, "r", encoding="utf-8") as f:
        return json.load(f)


def index_points_by_frame(points_doc: Optional[List[Dict[str, Any]]]) -> Dict[int, List[Dict[str, Any]]]:
    by_frame: Dict[int, List[Dict[str, Any]]] = {}
    if not points_doc:
        return by_frame
    for entry in points_doc:
        frame = int(entry.get("frame_idx", 0))
        by_frame.setdefault(frame, []).extend(entry.get("targets", []))
    return by_frame

def load_reference_tasks_from_task_info_dir(limit: int = 50) -> List[Dict[str, Any]]:
    base = os.path.join("code_gen", "task_info")
    refs: List[Dict[str, Any]] = []
    if not os.path.isdir(base):
        return refs
    for fname in os.listdir(base):
        if not fname.endswith(".jsonl"):
            continue
        fpath = os.path.join(base, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        if isinstance(obj, dict) and "task_description" in obj:
                            refs.append(obj)
                            if len(refs) >= limit:
                                return refs
                    except Exception:
                        continue
        except Exception:
            continue
    return refs

def load_reference_tasks_from_new_task_info(limit: int = 50) -> List[Dict[str, Any]]:
    refs: List[Dict[str, Any]] = []
    try:
        import sys
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)
        import code_gen.new_task_info as nti
        for k in dir(nti):
            if k.isupper():
                v = getattr(nti, k)
                if isinstance(v, dict) and "task_description" in v:
                    refs.append({"task_name": v.get("task_name", k.lower()), "task_description": v.get("task_description")})
                    if len(refs) >= limit:
                        break
    except Exception:
        pass
    return refs

def choose_reference_tasks(max_n: int = 12) -> List[Dict[str, Any]]:
    refs = load_reference_tasks_from_task_info_dir(limit=max_n)
    if len(refs) < max_n:
        extra = load_reference_tasks_from_new_task_info(limit=max_n - len(refs))
        refs.extend(extra)
    return refs[:max_n]

def build_action_with_real_points(step: Dict[str, Any], frame_points: List[Dict[str, Any]]) -> str:
    action_type = (step.get("action") or "").lower()
    names = step.get("target_name", []) or []
    pix_map = {}
    for rec in frame_points or []:
        nm = rec.get("target_name")
        px = rec.get("pixel")
        if nm is not None and isinstance(px, (list, tuple)) and len(px) >= 2:
            pix_map[nm] = (float(px[0]), float(px[1]))

    if action_type == "pick" and names:
        tgt = names[0]
        pt = pix_map.get(tgt) or (list(pix_map.values())[0] if pix_map else None)
        return f"<action>pick({tgt},({int(round(pt[0]))},{int(round(pt[1]))}))</action>" if pt else "<action>done()</action>"

    if action_type == "place" and len(names) >= 2:
        container = names[1]
        pt = pix_map.get(container) or (list(pix_map.values())[0] if pix_map else None)
        return f"<action>place({container},({int(round(pt[0]))},{int(round(pt[1]))}))</action>" if pt else "<action>done()</action>"

    if action_type == "done":
        return "<action>done()</action>"

    return "<action>done()</action>"


def list_episode_ids(subplan_dir: str) -> List[int]:
    eps = []
    if not os.path.isdir(subplan_dir):
        return eps
    for fn in os.listdir(subplan_dir):
        if fn.startswith("episode") and fn.endswith(".json"):
            try:
                eps.append(int(fn[len("episode"): -len(".json")]))
            except Exception:
                continue
    return sorted(eps)


def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, obj: Any):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


# ================================ Pipeline ================================
def annotate(
    task_name: str,
    task_config: str,
    model: str = "local",
    only_episode: Optional[int] = None,
) -> None:
    ref_tasks = choose_reference_tasks(max_n=12)
    subplan_dir = load_subplan_dir(task_name, task_config)
    episode_ids = [only_episode] if only_episode is not None else list_episode_ids(subplan_dir)

    for eid in episode_ids:
        subplan_path = os.path.join(subplan_dir, f"episode{eid}.json")
        if not os.path.exists(subplan_path):
            print(f"Skip episode {eid}: no subplan at {subplan_path}")
            continue
        subplan = read_json(subplan_path)

        # 1) Instruction for this episode (based on task_info)
        instr_msgs = build_instruction_prompt_from_refs(ref_tasks)
        try:
            instruction = gpt_agent(instr_msgs, model=model)
        except Exception as e:
            instruction = f"<INSTRUCTION_GENERATION_FAILED: {e}>"

        # 2) Reasoning for each subplan step
        points_doc = load_points_for_episode(task_name, task_config, eid)
        points_by_frame = index_points_by_frame(points_doc)

        step_outputs: List[Dict[str, Any]] = []
        for step in subplan:
            frame_idx = int(step.get("frame_idx", 0))
            candidates = points_by_frame.get(frame_idx, [])
            msgs = build_reasoning_prompt(ref_tasks, step, candidates)
            try:
                reasoning = gpt_agent(msgs, model=model)
            except Exception as e:
                reasoning = f"<REASONING_GENERATION_FAILED: {e}>"

            final_action = build_action_with_real_points(step, candidates)
            reasoning_and_action = f"{reasoning}\n{final_action}"

            step_outputs.append({
                "frame_idx": frame_idx,
                "subplan_step": step,
                "output": reasoning_and_action,
            })

        # Save per-episode annotations under robotwin_data/<task>/<config>/episodeX/
        epi_dir = os.path.join("robotwin_data", task_name, task_config, f"episode{eid}")
        save_json(os.path.join(epi_dir, "instruction.json"), {"instruction": instruction})
        save_json(os.path.join(epi_dir, "reasoning.json"), {"steps": step_outputs})
        print(f"Annotated episode {eid}: saved instruction.json and reasoning.json")


def main():
    parser = argparse.ArgumentParser(description="Annotate data using LLM: instruction + per-step reasoning/actions.")
    parser.add_argument("task_name", type=str)
    parser.add_argument("task_config", type=str)
    parser.add_argument("--model", type=str, default="local")
    parser.add_argument("--only_episode", type=int, default=None)
    args = parser.parse_args()

    annotate(
        task_name=args.task_name,
        task_config=args.task_config,
        model=args.model,
        only_episode=args.only_episode,
    )


if __name__ == "__main__":
    main()
