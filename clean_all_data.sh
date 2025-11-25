#!/bin/bash

# Base directories
SOURCE_BASE="robotwin_data/data_origin"
TARGET_BASE="robotwin_data/data"  # Can be changed to a different output directory
TASK_INFO="code_gen/task_info/common_sense_correction.jsonl"
TASKS=("9_safe_items_placement_correction")

# Camera types
CAMERAS=("front_camera" "front_left_camera" "front_right_camera")

# Find all task directories under data_origin
for task_dir in "$SOURCE_BASE"/*; do
# for task in "${TASKS[@]}"; do
#     task_dir="$SOURCE_BASE/$task"
    # Check if it's a directory
    if [ -d "$task_dir" ]; then
        # Get task name from directory path
        task_name=$(basename "$task_dir")

        echo "Processing task: $task_name"

        # Check if data_collect directory exists
        if [ -d "$task_dir/data_collect" ]; then
            # Process each camera
            for camera in "${CAMERAS[@]}"; do
                echo "  Processing camera: $camera"

                python script/auto_gen/clean_data_raw.py \
                    --source_dir "$task_dir/data_collect" \
                    --target_dir "$TARGET_BASE/$task_name/data_collect/$camera" \
                    --task_name "$task_name" \
                    --task_info "$TASK_INFO" \
                    --camera "$camera" \
                    --all

                if [ $? -eq 0 ]; then
                    echo "  ✓ Successfully processed $camera for $task_name"
                else
                    echo "  ✗ Failed to process $camera for $task_name"
                fi
            done
        else
            echo "  Warning: data_collect directory not found for $task_name"
        fi

        echo "----------------------------------------"
    fi
done

echo "All tasks completed!"
