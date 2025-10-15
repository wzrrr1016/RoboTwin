#!/bin/bash

# bash collect_data.sh <task_name> <task_config> <gpu_id>
# e.g. bash collect_data.sh pick_place_block_2r2b demo_randomized 0

task_name=${1}
task_config=${2}
gpu_id=${3}

./script/.update_path.sh > /dev/null 2>&1

export CUDA_VISIBLE_DEVICES=${gpu_id}

PYTHONWARNINGS=ignore::UserWarning \
python script/collect_data_save.py $task_name $task_config
rm -rf data/${task_name}/${task_config}/.cache
