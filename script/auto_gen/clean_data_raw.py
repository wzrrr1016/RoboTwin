#!/usr/bin/env python3
"""
Clean and convert raw data to target format.

This script converts data from source directory to target directory format by:
1. Generating plan.json with task_description and next_action
2. Generating points.json with 2D pixel coordinates
3. Saving frames to frames_raw and frames_points directories

Usage:
python script/auto_gen/clean_data_raw.py \
    --source_dir data/1_toy_and_metal_storage_correction/data_collect \
    --target_dir robotwin_data/1_toy_and_metal_storage_correction/data_collect/front_camera \
    --task_name 1_toy_and_metal_storage_correction \
    --task_info code_gen/task_info/common_sense_correction.jsonl \
    --camera front_camera \
    --all

    Or use full path for task_name (will auto-extract short name):
python script/auto_gen/clean_data_raw.py \
    --source_dir data/common_sense_correction/1_non_drinkware_placement_correction/demo_randomized \
    --target_dir robotwin_data/common_sense_correction/1_non_drinkware_placement_correction/demo_randomized \
    --task_name common_sense_correction/1_non_drinkware_placement_correction \
    --task_info code_gen/task_info/common_sense_correction.jsonl \
    --episode 0
"""

import os
import sys
import json
import argparse
import h5py

# Add project root to path
sys.path.append("./")

from envs.utils.grasp_pose import world_to_pixel
from script.auto_gen.utils.common import load_task_info, parse_task_actions, load_subplan
from script.auto_gen.utils.plan_generator import generate_plan
from script.auto_gen.utils.point_generator import generate_points_and_frames


def process_episode(
    source_dir: str,
    target_dir: str,
    task_name: str,
    task_info_path: str,
    episode_id: int,
    camera_name: str = "front_camera",
):
    """
    Process a single episode.

    Args:
        source_dir: Source data directory (e.g., data/.../demo_randomized)
        target_dir: Target output directory (e.g., robotwin_data/.../demo_randomized)
        task_name: Task name for looking up in task_info
        task_info_path: Path to task info jsonl file
        episode_id: Episode ID to process
        camera_name: Camera name to use
    """
    # Construct paths
    subplan_path = os.path.join(source_dir, "sub_plan", f"episode{episode_id}.json")
    hdf5_path = os.path.join(source_dir, "data", f"episode{episode_id}.hdf5")
    output_dir = os.path.join(target_dir, f"episode{episode_id}")

    # Validate input files
    if not os.path.exists(subplan_path):
        raise FileNotFoundError(f"Subplan not found: {subplan_path}")
    if not os.path.exists(hdf5_path):
        raise FileNotFoundError(f"HDF5 data not found: {hdf5_path}")

    print(f"Processing episode {episode_id}...")
    print(f"  Source: {source_dir}")
    print(f"  Target: {output_dir}")

    # Extract short task name if full path is provided
    # e.g., "common_sense_correction/1_non_drinkware_placement_correction" -> "1_non_drinkware_placement_correction"
    short_task_name = task_name.split('/')[-1] if '/' in task_name else task_name
    print(f"  Task name: {short_task_name}")

    # Load task info and extract action descriptions
    task_info = load_task_info(task_info_path, short_task_name)
    action_descriptions = parse_task_actions(task_info['task_description'])
    print(f"  Found {len(action_descriptions)} action descriptions")

    # Load subplan
    subplan = load_subplan(subplan_path)
    print(f"  Loaded {len(subplan)} subplan entries")

    # Generate plan with task_description and next_action
    plan = generate_plan(subplan, action_descriptions)

    # Get the last frame index
    with h5py.File(hdf5_path, "r") as root:
        K_seq = root[f"/observation/{camera_name}/intrinsic_cv"][()]  # [T,3,3]
    last_frame_idx = int(K_seq.shape[0] - 1)

    done_task = {
        'frame_idx': last_frame_idx,
        'action': 'done',
        'target_name': [],
        'pose': {},
        'task_description': 'Task completed',
        'next_action': {
            'action': 'done',
            'target': []
        }
    }

    plan.append(done_task)
    print(f"  Generated plan with {len(plan)} entries")
    
    # Generate points and save frames
    points_list = generate_points_and_frames(
        plan, hdf5_path, camera_name, output_dir, world_to_pixel
    )
    print(f"  Generated {len(points_list)} point entries")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Save plan.json
    for entry in plan:
        if 'pose' in entry:
            del entry['pose']  # Remove pose before saving
    plan_path = os.path.join(output_dir, "plan.json")
    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    print(f"  Saved plan.json")

    # Save points.json
    points_path = os.path.join(output_dir, "points.json")
    with open(points_path, 'w', encoding='utf-8') as f:
        json.dump(points_list, f, ensure_ascii=False, indent=2)
    print(f"  Saved points.json")

    print(f"Successfully processed episode {episode_id}")
    print(f"  Output directory: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Clean and convert raw data to target format"
    )
    parser.add_argument(
        "--source_dir",
        type=str,
        required=True,
        help="Source data directory (e.g., data/common_sense_correction/1_non_drinkware_placement_correction/demo_randomized)"
    )
    parser.add_argument(
        "--target_dir",
        type=str,
        required=True,
        help="Target output directory (e.g., robotwin_data/common_sense_correction/1_non_drinkware_placement_correction/demo_randomized)"
    )
    parser.add_argument(
        "--task_name",
        type=str,
        required=True,
        help="Task name for task_info lookup (e.g., common_sense_correction/1_non_drinkware_placement_correction)"
    )
    parser.add_argument(
        "--task_info",
        type=str,
        default="code_gen/task_info/common_sense_correction.jsonl",
        help="Path to task info jsonl file"
    )
    parser.add_argument(
        "--episode",
        type=int,
        default=0,
        help="Episode ID to process"
    )
    parser.add_argument(
        "--camera",
        type=str,
        default="front_camera",
        help="Camera name to use"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all episodes in the source directory"
    )

    args = parser.parse_args()

    if args.all:
        episodes = range(len(os.listdir(os.path.join(args.source_dir, "data"))))
    else:
        episodes = [args.episode]

    for episode in episodes:
        process_episode(
            source_dir=args.source_dir,
            target_dir=args.target_dir,
            task_name=args.task_name,
            task_info_path=args.task_info,
            episode_id=episode,
            camera_name=args.camera,
        )

    args = parser.parse_args()

    process_episode(
        source_dir=args.source_dir,
        target_dir=args.target_dir,
        task_name=args.task_name,
        task_info_path=args.task_info,
        episode_id=args.episode,
        camera_name=args.camera,
    )


if __name__ == "__main__":
    main()
