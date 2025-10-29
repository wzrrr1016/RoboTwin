import os
import json
import argparse
from typing import Any, Dict, List, Optional, Tuple


# ============== Plug-in LLM Caller (replace with your gpt_agent) ==============
def gpt_agent(messages: List[Dict[str, str]], model: str = "local") -> str:
    """Use code_gen/gpt_agent.py local backend to generate text."""
    # Defer import to avoid global dependency when unused
    from code_gen.gpt_agent import generate
    # The local gpt_agent ignores the model string and uses its own MODEL path
    return generate(messages, gpt="local", temperature=0)


# ============================ Prompt Builders =============================
def build_instruction_prompt(task_info: Dict[str, Any]) -> List[Dict[str, str]]:
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

    user = (
        "Given the following task_info (JSON), write a single instruction that\n"
        "guides the agent implicitly. Avoid direct step descriptions and avoid any\n"
        "error correction content.\n\n"
        f"task_info:\n{json.dumps(task_info, ensure_ascii=False, indent=2)}\n"
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def build_reasoning_prompt(
    task_info: Dict[str, Any],
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
        "When given a subplan step, provide concise reasoning (why this step is needed)\n"
        "and then output exactly one final action wrapped in <action>...</action>.\n"
        "Allowed actions:\n"
        "1. pick(target, point)\n2. place(container, point)\n3. done()\n"
        "Constraints:\n"
        "- The final action must be the last line and be wrapped by <action> tags.\n"
        "- Do not include any correction or critique content.\n"
        "- If a pixel point is provided for a target/container, use it verbatim."
    )

    # Normalize candidate points (list of dicts with fields: target_name, pixel)
    cand_desc = ""
    if candidate_points:
        compact = [
            {"name": c.get("target_name"), "pixel": c.get("pixel")} for c in candidate_points
        ]
        cand_desc = f"\n\nCandidate points (if applicable):\n{json.dumps(compact, ensure_ascii=False)}"

    user = (
        "Given task_info and the following subplan step, reason about why this step is done\n"
        "and then choose exactly one action from the allowed set.\n\n"
        f"task_info (JSON):\n{json.dumps(task_info, ensure_ascii=False, indent=2)}\n\n"
        f"subplan_step (JSON):\n{json.dumps(subplan_step, ensure_ascii=False, indent=2)}\n"
        f"{cand_desc}\n\n"
        "Remember: the final line must be <action>...</action>."
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
    task_info_path: str,
    model: str = "local",
    only_episode: Optional[int] = None,
) -> None:
    task_info = read_json(task_info_path)
    subplan_dir = load_subplan_dir(task_name, task_config)
    episode_ids = [only_episode] if only_episode is not None else list_episode_ids(subplan_dir)

    for eid in episode_ids:
        subplan_path = os.path.join(subplan_dir, f"episode{eid}.json")
        if not os.path.exists(subplan_path):
            print(f"Skip episode {eid}: no subplan at {subplan_path}")
            continue
        subplan = read_json(subplan_path)

        # 1) Instruction for this episode (based on task_info)
        instr_msgs = build_instruction_prompt(task_info)
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
            msgs = build_reasoning_prompt(task_info, step, candidates)
            try:
                reasoning_and_action = gpt_agent(msgs, model=model)
            except Exception as e:
                reasoning_and_action = f"<REASONING_GENERATION_FAILED: {e}>\n<action>done()</action>"

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
    parser.add_argument("task_info_path", type=str, help="Path to task_info JSON (e.g., scene_info.json)")
    parser.add_argument("--model", type=str, default="local")
    parser.add_argument("--only_episode", type=int, default=None)
    args = parser.parse_args()

    annotate(
        task_name=args.task_name,
        task_config=args.task_config,
        task_info_path=args.task_info_path,
        model=args.model,
        only_episode=args.only_episode,
    )


if __name__ == "__main__":
    main()
