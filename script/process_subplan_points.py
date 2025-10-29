import os
import sys
import json
import argparse
from typing import Dict, Any, List, Tuple, DefaultDict
from collections import defaultdict

import numpy as np
import h5py
import cv2

# Allow importing project utilities
sys.path.append("./")
from envs.utils.grasp_pose import world_to_pixel, pixel_to_world  # reuse existing, proven math


def load_episode_paths(task_name: str, task_config: str) -> Dict[str, str]:
    base = os.path.join("data", task_name, task_config)
    return {
        "hdf5_dir": os.path.join(base, "data"),
        "subplan_dir": os.path.join(base, "sub_plan"),
    }


def list_episode_ids(subplan_dir: str) -> List[int]:
    eps = []
    if not os.path.isdir(subplan_dir):
        return eps
    for fn in os.listdir(subplan_dir):
        if fn.startswith("episode") and fn.endswith(".json"):
            try:
                eid = int(fn[len("episode"): -len(".json")])
                eps.append(eid)
            except Exception:
                continue
    return sorted(eps)


def read_subplan(subplan_path: str) -> List[Dict[str, Any]]:
    with open(subplan_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_rgb_at(root: h5py.File, camera_name: str, frame_idx: int) -> np.ndarray:
    rgb_ds_path = f"/observation/{camera_name}/rgb"
    if rgb_ds_path not in root:
        raise RuntimeError(f"Missing RGB dataset: {rgb_ds_path}")
    rgb_bytes = root[rgb_ds_path][frame_idx].tobytes()
    arr = np.frombuffer(rgb_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # BGR
    if img is None:
        raise RuntimeError(f"Failed to decode RGB frame {frame_idx} for {camera_name}")
    return img


def compute_points_for_subplan(
    subplan: List[Dict[str, Any]],
    hdf5_path: str,
    camera_name: str,
) -> Tuple[List[Dict[str, Any]], DefaultDict[int, List[Dict[str, Any]]]]:
    results: List[Dict[str, Any]] = []
    points_by_frame: DefaultDict[int, List[Dict[str, Any]]] = defaultdict(list)
    with h5py.File(hdf5_path, "r") as root:
        # Fetch intrinsics/extrinsics sequences and depth images
        try:
            K_seq = root[f"/observation/{camera_name}/intrinsic_cv"][()]  # [T,3,3]
            Tcw_seq = root[f"/observation/{camera_name}/cam2world_gl"][()]  # [T,4,4]
        except KeyError as e:
            raise RuntimeError(f"Missing camera config in {hdf5_path}: {e}")

        # Depth may be optional; use if available
        depth_seq = None
        if f"/observation/{camera_name}/depth" in root:
            depth_seq = root[f"/observation/{camera_name}/depth"][()]  # [T,H,W]

        # For each subplan entry, compute point(s) for target_name(s)
        for entry in subplan:
            frame_idx = int(entry.get("frame_idx", 0))
            action = entry.get("action", "")
            targets: List[str] = entry.get("target_name", []) or []
            pose_map: Dict[str, Any] = entry.get("pose", {})

            # Guard against out-of-range
            if frame_idx < 0 or frame_idx >= K_seq.shape[0]:
                # skip invalid frame
                continue

            K = np.array(K_seq[frame_idx])
            Tcw = np.array(Tcw_seq[frame_idx])

            target_points: List[Dict[str, Any]] = []
            for name in targets:
                if name not in pose_map:
                    continue
                world_p = np.array(pose_map[name], dtype=float)  # [x,y,z]

                # Project to image pixel
                px = world_to_pixel(world_p, Tcw, K)[0]
                u, v = float(px[0]), float(px[1])

                # Optionally recover world point from depth at that pixel (if depth available)
                world_from_depth = None
                if depth_seq is not None:
                    depth_img = np.array(depth_seq[frame_idx])
                    uu = int(np.clip(np.round(u), 0, depth_img.shape[1] - 1))
                    vv = int(np.clip(np.round(v), 0, depth_img.shape[0] - 1))
                    world_pt = pixel_to_world([uu, vv], Tcw, K, depth_img)[0]
                    world_from_depth = world_pt.tolist()

                record = {
                    "target_name": name,
                    "pixel": [u, v],
                    "world_from_depth": world_from_depth,
                    "world_pose": world_p.tolist(),
                }
                target_points.append(record)
                points_by_frame[frame_idx].append(record)

            results.append({
                "frame_idx": frame_idx,
                "action": action,
                "camera": camera_name,
                "targets": target_points,
            })

    return results, points_by_frame


def save_episode_package(
    robotwin_data_dir: str,
    task_name: str,
    task_config: str,
    episode_id: int,
    plan: List[Dict[str, Any]],
    points: List[Dict[str, Any]],
    points_by_frame: DefaultDict[int, List[Dict[str, Any]]],
    hdf5_path: str,
    camera_name: str,
):
    epi_dir = os.path.join(robotwin_data_dir, task_name, task_config, f"episode{episode_id}")
    raw_dir = os.path.join(epi_dir, "frames_raw")
    pts_dir = os.path.join(epi_dir, "frames_points")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(pts_dir, exist_ok=True)

    # Save plan and points json
    with open(os.path.join(epi_dir, "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    with open(os.path.join(epi_dir, "points.json"), "w", encoding="utf-8") as f:
        json.dump(points, f, ensure_ascii=False, indent=2)

    # Draw points on required frames and save raw + overlay
    color_cycle = [
        (0, 0, 255),    # red
        (0, 255, 0),    # green
        (255, 0, 0),    # blue
        (0, 255, 255),  # yellow
        (255, 0, 255),  # magenta
        (255, 255, 0),  # cyan
        (128, 0, 255),
        (0, 128, 255),
    ]

    with h5py.File(hdf5_path, "r") as root:
        # Frames required: any frame present in plan or points_by_frame
        frames_needed = set(points_by_frame.keys()) | {int(p.get("frame_idx", 0)) for p in plan}
        for frame_idx in sorted(frames_needed):
            try:
                img = decode_rgb_at(root, camera_name, frame_idx)
            except Exception:
                continue

            raw_path = os.path.join(raw_dir, f"frame_{frame_idx:06d}.png")
            cv2.imwrite(raw_path, img)

            overlay = img.copy()
            for i, tgt in enumerate(points_by_frame.get(frame_idx, [])):
                u, v = tgt["pixel"]
                color = color_cycle[i % len(color_cycle)]
                uu = int(round(u))
                vv = int(round(v))
                cv2.circle(overlay, (uu, vv), 6, color, thickness=-1)
                label = str(tgt.get("target_name", ""))
                cv2.putText(overlay, label, (uu + 8, vv - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

            pts_path = os.path.join(pts_dir, f"frame_{frame_idx:06d}.png")
            cv2.imwrite(pts_path, overlay)


def main():
    parser = argparse.ArgumentParser(description="Extract subplan frame points using intrinsics and depth")
    parser.add_argument("task_name", type=str, help="Task name (e.g., pick_place_block)")
    parser.add_argument("task_config", type=str, help="Task config (e.g., demo_randomized)")
    parser.add_argument("--camera", type=str, default="front_camera", help="Camera name to use")
    parser.add_argument("--robotwin_data", type=str, default="robotwin_data", help="Output base dir (symlink exists)")
    parser.add_argument("--only_episode", type=int, default=None, help="Process only this episode id")
    args = parser.parse_args()

    paths = load_episode_paths(args.task_name, args.task_config)
    episode_ids = list_episode_ids(paths["subplan_dir"]) if args.only_episode is None else [args.only_episode]
    if not episode_ids:
        print(f"No subplan files found under {paths['subplan_dir']}")
        return

    for eid in episode_ids:
        subplan_path = os.path.join(paths["subplan_dir"], f"episode{eid}.json")
        hdf5_path = os.path.join(paths["hdf5_dir"], f"episode{eid}.hdf5")
        if not os.path.exists(hdf5_path):
            print(f"Skip episode {eid}: missing hdf5 {hdf5_path}")
            continue
        subplan = read_subplan(subplan_path)
        try:
            results, points_by_frame = compute_points_for_subplan(subplan, hdf5_path, args.camera)
        except Exception as e:
            print(f"Error processing episode {eid}: {e}")
            continue
        save_episode_package(
            args.robotwin_data,
            args.task_name,
            args.task_config,
            eid,
            subplan,
            results,
            points_by_frame,
            hdf5_path,
            args.camera,
        )
        print(f"Saved episode {eid} package")


if __name__ == "__main__":
    main()
