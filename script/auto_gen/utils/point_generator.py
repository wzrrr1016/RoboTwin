"""Point and frame generation utilities."""

import os
from typing import Dict, Any, List, Tuple
from collections import defaultdict

import numpy as np
import h5py
import cv2


def compute_points_for_plan(
    plan: List[Dict[str, Any]],
    hdf5_path: str,
    camera_name: str,
    world_to_pixel_func,
    original_subplan: List[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], Dict[int, Dict[str, List[float]]]]:
    """
    Compute 2D points for each target in the plan.

    Special rule: If container is 'table', use object's x, y but z = 0.743

    Args:
        plan: List of plan entries (without pose field)
        hdf5_path: Path to HDF5 data file
        camera_name: Camera name to use
        world_to_pixel_func: Function to convert world coordinates to pixel
        original_subplan: Original subplan with pose data (needed for point generation)

    Returns:
        Tuple of (points_list, points_by_frame)
        - points_list: List of {frame_idx, points} dicts
        - points_by_frame: Dict mapping frame_idx to {name: [u, v]}
    """
    points_list = []
    points_by_frame = defaultdict(dict)

    # Create frame_idx to pose map from original subplan
    frame_to_pose = {}
    if original_subplan:
        for sub_entry in original_subplan:
            frame_idx = sub_entry.get('frame_idx', 0)
            if 'pose' in sub_entry:
                frame_to_pose[frame_idx] = sub_entry['pose']

    with h5py.File(hdf5_path, "r") as root:
        try:
            K_seq = root[f"/observation/{camera_name}/intrinsic_cv"][()]
            Tcw_seq = root[f"/observation/{camera_name}/cam2world_gl"][()]
        except KeyError as e:
            raise RuntimeError(f"Missing camera config in {hdf5_path}: {e}")

        for idx in range(len(plan)):
            entry = plan[idx]
            frame_idx = int(entry.get("frame_idx", 0))
            action = entry['next_action']['action']
            targets = entry["next_action"]['target']
            if frame_idx < 0 or frame_idx >= K_seq.shape[0]:
                continue

            K = np.array(K_seq[frame_idx])
            Tcw = np.array(Tcw_seq[frame_idx])

            # Get pose data from original subplan
            pose_map = entry['pose']

            frame_points = {}

            # Handle different cases based on action and targets
            if action == 'pick':
                # For pick action, just project the object
                for name in targets:
                    if name not in pose_map:
                        continue
                    world_p = np.array(pose_map[name], dtype=float)
                    px = world_to_pixel_func(world_p, Tcw, K)[0]
                    u, v = float(px[0]), float(px[1])
                    frame_points[name] = [u, v]

            elif action == 'place':
                # For place action with table as container
                if len(targets) == 2:
                    obj_name, container_name = targets[0], targets[1]

                    # Add object point
                    if obj_name in pose_map:
                        obj_pos = np.array(pose_map[obj_name], dtype=float)
                        px = world_to_pixel_func(obj_pos, Tcw, K)[0]
                        u, v = float(px[0]), float(px[1])
                        frame_points[obj_name] = [u, v]

                    # Add container point
                    if container_name == 'table':
                        # Use object's x, y but z = 0.743
                        next_entry = plan[idx+1]
                        print("table next:",next_entry)
                        if next_entry['action'] == 'pick' and next_entry['target_name'][0] == obj_name:
                            if obj_name in pose_map:
                                obj_pos = np.array(pose_map[obj_name], dtype=float)
                                table_point = np.array([obj_pos[0], obj_pos[1], 0.745])
                                px = world_to_pixel_func(table_point, Tcw, K)[0]
                                u, v = float(px[0]), float(px[1])
                                frame_points['table'] = [u, v]
                        else:
                            next_pose_map = next_entry['pose']
                            if obj_name in next_pose_map:
                                obj_pos = np.array(next_pose_map[obj_name], dtype=float)
                                table_point = np.array([obj_pos[0], obj_pos[1], 0.745])
                                px = world_to_pixel_func(table_point, Tcw, K)[0]
                                u, v = float(px[0]), float(px[1])
                                frame_points['table'] = [u, v]                            
                    else:
                        # Normal container
                        next_pose_map = plan[idx+1]['pose']
                        if obj_name in next_pose_map:
                            obj_pos = np.array(next_pose_map[obj_name], dtype=float)
                            container_point = np.array([obj_pos[0], obj_pos[1], 0.745])
                            px = world_to_pixel_func(container_point, Tcw, K)[0]
                            u, v = float(px[0]), float(px[1])
                            frame_points[container_name] = [u, v] 
                        elif container_name in pose_map:
                            container_pos = np.array(pose_map[container_name], dtype=float)
                            px = world_to_pixel_func(container_pos, Tcw, K)[0]
                            u, v = float(px[0]), float(px[1])
                            frame_points[container_name] = [u, v]
            else:
                frame_points = {}
                
            points_list.append({
                "frame_idx": frame_idx,
                "points": frame_points
            })
            points_by_frame[frame_idx] = frame_points

    return points_list, points_by_frame


def save_frames(
    plan: List[Dict[str, Any]],
    points_by_frame: Dict[int, Dict[str, List[float]]],
    hdf5_path: str,
    camera_name: str,
    output_dir: str,
):
    """
    Save frame images to frames_raw and frames_points directories.

    Args:
        plan: List of plan entries
        points_by_frame: Dict mapping frame_idx to points
        hdf5_path: Path to HDF5 data file
        camera_name: Camera name to use
        output_dir: Output directory for frames
    """
    raw_dir = os.path.join(output_dir, "frames_raw")
    pts_dir = os.path.join(output_dir, "frames_points")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(pts_dir, exist_ok=True)

    color_cycle = [
        (0, 0, 255),    # red
        (0, 255, 0),    # green
        (255, 0, 0),    # blue
        (0, 255, 255),  # yellow
        (255, 0, 255),  # magenta
        (255, 255, 0),  # cyan
    ]

    with h5py.File(hdf5_path, "r") as root:
        frames_needed = set(points_by_frame.keys()) | {int(p.get("frame_idx", 0)) for p in plan}

        for frame_idx in sorted(frames_needed):
            try:
                rgb_ds_path = f"/observation/{camera_name}/rgb"
                rgb_bytes = root[rgb_ds_path][frame_idx].tobytes()
                arr = np.frombuffer(rgb_bytes, dtype=np.uint8)
                img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if img is None:
                    continue
            except Exception as e:
                print(f"Warning: Could not read frame {frame_idx}: {e}")
                continue

            # Save raw frame
            raw_path = os.path.join(raw_dir, f"frame_{frame_idx:06d}.png")
            cv2.imwrite(raw_path, img)

            # Save frame with points
            overlay = img.copy()
            frame_pts = points_by_frame.get(frame_idx, {})
            for i, (name, (u, v)) in enumerate(frame_pts.items()):
                color = color_cycle[i % len(color_cycle)]
                uu = int(round(u))
                vv = int(round(v))
                cv2.circle(overlay, (uu, vv), 6, color, thickness=-1)
                cv2.putText(overlay, name, (uu + 8, vv - 8),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

            pts_path = os.path.join(pts_dir, f"frame_{frame_idx:06d}.png")
            cv2.imwrite(pts_path, overlay)


def generate_points_and_frames(
    plan: List[Dict[str, Any]],
    hdf5_path: str,
    camera_name: str,
    output_dir: str,
    world_to_pixel_func,
    original_subplan: List[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate points and save frames.

    This is the main entry point for point and frame generation.

    Args:
        plan: List of plan entries (without pose)
        hdf5_path: Path to HDF5 data file
        camera_name: Camera name to use
        output_dir: Output directory
        world_to_pixel_func: Function to convert world coordinates to pixel
        original_subplan: Original subplan with pose data (needed for point generation)

    Returns:
        List of points with frame_idx
    """
    # Compute 2D points (pass original subplan for pose data)
    points_list, points_by_frame = compute_points_for_plan(
        plan, hdf5_path, camera_name, world_to_pixel_func, original_subplan
    )

    # Save frames
    save_frames(plan, points_by_frame, hdf5_path, camera_name, output_dir)

    return points_list
