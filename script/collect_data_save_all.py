import sys

sys.path.append("./")

import sapien.core as sapien
from sapien.render import clear_cache
from collections import OrderedDict
import pdb
from envs import *
from envs.zerograsp.zerograsp import ZeroGrasp_Getter
import yaml
import importlib
import pkgutil
import json
import traceback
import os
import time
from argparse import ArgumentParser
import warnings
warnings.filterwarnings("ignore")


current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)


def class_decorator(task_name):
    import re

    # Convert old format to new format if needed
    # e.g., "1_healthy_food_organization_correction" -> "healthy_food_organization_correction_1"
    original_task_name = task_name
    match = re.match(r'^(\d+)_(.+)$', task_name)
    if match:
        number = match.group(1)
        name_part = match.group(2)
        # Both module name and class name use the new format
        module_name = f"{number}_{name_part}"
        class_name = f"{name_part}_{number}"
    else:
        module_name = task_name
        class_name = task_name

    # Try direct import first: envs.<module_name>
    try:
        envs_module = importlib.import_module(f"envs.{module_name}")
        env_class = getattr(envs_module, class_name)
        return env_class()
    except Exception:
        pass

    # Try with subdirectory: envs.common_sense_correction.<module_name>
    try:
        envs_module = importlib.import_module(f"envs.common_sense_correction.{module_name}")
        env_class = getattr(envs_module, class_name)
        return env_class()
    except Exception:
        pass

    # Fallback: recursively search all submodules under envs for a class named class_name or task_name
    import envs as envs_pkg
    prefix = envs_pkg.__name__ + "."
    for finder, name, ispkg in pkgutil.walk_packages(envs_pkg.__path__, prefix):
        try:
            mod = importlib.import_module(name)
            # Try the converted class name first
            if hasattr(mod, class_name):
                env_class = getattr(mod, class_name)
                return env_class()
            # Fall back to original task name
            if hasattr(mod, task_name):
                env_class = getattr(mod, task_name)
                return env_class()
        except Exception:
            continue
    raise SystemExit(f"No such task: {original_task_name} (module: {module_name}, class: {class_name})")


def get_embodiment_config(robot_file):
    robot_config_file = os.path.join(robot_file, "config.yml")
    with open(robot_config_file, "r", encoding="utf-8") as f:
        embodiment_args = yaml.load(f.read(), Loader=yaml.FullLoader)
    return embodiment_args


def main(task_name=None, task_config=None):

    task = class_decorator(task_name)
    config_path = f"./task_config/{task_config}.yml"

    with open(config_path, "r", encoding="utf-8") as f:
        args = yaml.load(f.read(), Loader=yaml.FullLoader)

    args['task_name'] = task_name

    embodiment_type = args.get("embodiment")
    embodiment_config_path = os.path.join(CONFIGS_PATH, "_embodiment_config.yml")

    with open(embodiment_config_path, "r", encoding="utf-8") as f:
        _embodiment_types = yaml.load(f.read(), Loader=yaml.FullLoader)

    def get_embodiment_file(embodiment_type):
        robot_file = _embodiment_types[embodiment_type]["file_path"]
        if robot_file is None:
            raise "missing embodiment files"
        return robot_file

    if len(embodiment_type) == 1:
        args["left_robot_file"] = get_embodiment_file(embodiment_type[0])
        args["right_robot_file"] = get_embodiment_file(embodiment_type[0])
        args["dual_arm_embodied"] = True
    elif len(embodiment_type) == 3:
        args["left_robot_file"] = get_embodiment_file(embodiment_type[0])
        args["right_robot_file"] = get_embodiment_file(embodiment_type[1])
        args["embodiment_dis"] = embodiment_type[2]
        args["dual_arm_embodied"] = False
    else:
        raise "number of embodiment config parameters should be 1 or 3"

    args["left_embodiment_config"] = get_embodiment_config(args["left_robot_file"])
    args["right_embodiment_config"] = get_embodiment_config(args["right_robot_file"])

    if len(embodiment_type) == 1:
        embodiment_name = str(embodiment_type[0])
    else:
        embodiment_name = str(embodiment_type[0]) + "+" + str(embodiment_type[1])

    # show config
    print("============= Config =============\n")
    print("\033[95mMessy Table:\033[0m " + str(args["domain_randomization"]["cluttered_table"]))
    print("\033[95mRandom Background:\033[0m " + str(args["domain_randomization"]["random_background"]))
    if args["domain_randomization"]["random_background"]:
        print(" - Clean Background Rate: " + str(args["domain_randomization"]["clean_background_rate"]))
    print("\033[95mRandom Light:\033[0m " + str(args["domain_randomization"]["random_light"]))
    if args["domain_randomization"]["random_light"]:
        print(" - Crazy Random Light Rate: " + str(args["domain_randomization"]["crazy_random_light_rate"]))
    print("\033[95mRandom Table Height:\033[0m " + str(args["domain_randomization"]["random_table_height"]))
    print("\033[95mRandom Head Camera Distance:\033[0m " + str(args["domain_randomization"]["random_head_camera_dis"]))

    print("\033[94mHead Camera Config:\033[0m " + str(args["camera"]["head_camera_type"]) + f", " +
          str(args["camera"]["collect_head_camera"]))
    print("\033[94mWrist Camera Config:\033[0m " + str(args["camera"]["wrist_camera_type"]) + f", " +
          str(args["camera"]["collect_wrist_camera"]))
    print("\033[94mEmbodiment Config:\033[0m " + embodiment_name)
    print("\n==================================")

    args["embodiment_name"] = embodiment_name
    args['task_config'] = task_config
    args["save_path"] = os.path.join(args["save_path"], str(args["task_name"]), args["task_config"])
    run(task, args)


def run(TASK_ENV, args):
    epid, suc_num, fail_num, seed_list = 0, 0, 0, []



    zerograsp_config_path = args.get("zerograsp_config_path")
    zerograsp_checkpoint_path = args.get("zerograsp_checkpoint_path")


    grasp_getter = ZeroGrasp_Getter(zerograsp_config_path,zerograsp_checkpoint_path)
    # grasp_getter = None

    print(f"Task Name: \033[34m{args['task_name']}\033[0m")

    # =========== Collect Seed ===========
    os.makedirs(args["save_path"], exist_ok=True)

    os.makedirs(os.path.join(args["save_path"], "sub_plan"),exist_ok=True)


    def exist_hdf5(idx):
        file_path = os.path.join(args["save_path"], 'data', f'episode{idx}.hdf5')
        return os.path.exists(file_path)
    
    def exist_pkl(idx):
        file_path = os.path.join(args["save_path"], '_traj_data', f'episode{idx}.pkl')
        return os.path.exists(file_path)

    if not args["use_seed"]:
        print("\033[93m" + "[Start Seed and Pre Motion Data Collection]" + "\033[0m")
        args["need_plan"] = True

        if os.path.exists(os.path.join(args["save_path"], "seed.txt")):
            with open(os.path.join(args["save_path"], "seed.txt"), "r") as file:
                seed_list = file.read().split()
                if len(seed_list) != 0:
                    seed_list = [int(i) for i in seed_list]
                    suc_num = len(seed_list)
                    epid = max(seed_list) + 1
            print(f"Exist seed file, Start from: {epid} / {suc_num}")

        origin_args = args.copy()
        ct = 0
        while ct < suc_num:
            # print(exist_hdf5(ct), exist_pkl(ct))
            if (not exist_hdf5(ct)) and exist_pkl(ct):
                print(f"Collecting Data of episode {ct} (seed = {seed_list[ct]})")
                args["need_plan"] = False
                args["render_freq"] = 0
                args["save_data"] = True
                TASK_ENV.setup_demo(now_ep_num=ct, seed=seed_list[ct],grasp_getter=grasp_getter, **args)

                traj_data = TASK_ENV.load_tran_data(ct)
                args["left_joint_path"] = traj_data["left_joint_path"]
                args["right_joint_path"] = traj_data["right_joint_path"]
                TASK_ENV.set_path_lst(args)

                info_file_path = os.path.join(args["save_path"], "scene_info.json")

                if not os.path.exists(info_file_path):
                    with open(info_file_path, "w", encoding="utf-8") as file:
                        json.dump({}, file, ensure_ascii=False)

                with open(info_file_path, "r", encoding="utf-8") as file:
                    info_db = json.load(file)

                info = TASK_ENV.play_once()
                info_db[f"episode_{ct}"] = info

                with open(info_file_path, "w", encoding="utf-8") as file:
                    json.dump(info_db, file, ensure_ascii=False, indent=4)

                sub_plans = TASK_ENV.get_subplans()
                subplan_save_path = os.path.join(args["save_path"], "sub_plan", f"episode{ct}.json")
                # print(sub_plans)
                with open(subplan_save_path, "w", encoding="utf-8") as file:
                    json.dump(sub_plans, file, ensure_ascii=False, indent=4)

                TASK_ENV.close_env()
                TASK_ENV.merge_pkl_to_hdf5_video()
                TASK_ENV.remove_data_cache()

                clear_cache()
            ct += 1

        # clear_cache_freq = args["clear_cache_freq"]
        while suc_num < args["episode_num"]:
            try:

                args = origin_args.copy()
                args["save_data"] = True
                args["render_freq"] = 0
                print(f"Start Collecting Data of episode {suc_num} (seed = {epid})")
                TASK_ENV.setup_demo(now_ep_num=suc_num, seed=epid,grasp_getter=grasp_getter, **args)
                info = TASK_ENV.play_once()

                if TASK_ENV.plan_success and TASK_ENV.check_success():
                # if True:
                    print(f"simulate data episode {suc_num} success! (seed = {epid})")
                    seed_list.append(epid)

                    info_file_path = os.path.join(args["save_path"], "scene_info.json")

                    if not os.path.exists(info_file_path):
                        with open(info_file_path, "w", encoding="utf-8") as file:
                            json.dump({}, file, ensure_ascii=False)

                    with open(info_file_path, "r", encoding="utf-8") as file:
                        info_db = json.load(file)

                    info_db[f"episode_{suc_num}"] = info

                    with open(info_file_path, "w", encoding="utf-8") as file:
                        json.dump(info_db, file, ensure_ascii=False, indent=4)

                    sub_plans = TASK_ENV.get_subplans()
                    subplan_save_path = os.path.join(args["save_path"], "sub_plan", f"episode{suc_num}.json")
                    # print(sub_plans)
                    with open(subplan_save_path, "w", encoding="utf-8") as file:
                        json.dump(sub_plans, file, ensure_ascii=False, indent=4)

                    TASK_ENV.close_env()
                    TASK_ENV.merge_pkl_to_hdf5_video()
                    TASK_ENV.remove_data_cache()

                    suc_num += 1
                    clear_cache()
                
                else:
                    print(f"simulate data episode {suc_num} fail! (seed = {epid})")
                    fail_num += 1

                TASK_ENV.close_env()

                if args["render_freq"]:
                    TASK_ENV.viewer.close()
                clear_cache()
            except UnStableError as e:
                print(" -------------")
                print(f"simulate data episode {suc_num} fail! (seed = {epid})")
                print("Error: ", e)
                print(" -------------")
                fail_num += 1
                TASK_ENV.close_env()

                if args["render_freq"]:
                    TASK_ENV.viewer.close()
                clear_cache()
                time.sleep(0.3)
            except Exception as e:
                # stack_trace = traceback.format_exc()
                print(" -------------")
                print(f"simulate data episode {suc_num} fail! (seed = {epid})")
                print("Error: ", e)
                print(" -------------")
                fail_num += 1
                TASK_ENV.close_env()

                if args["render_freq"]:
                    TASK_ENV.viewer.close()
                time.sleep(1)
                clear_cache()
            epid += 1

            with open(os.path.join(args["save_path"], "seed.txt"), "w") as file:
                for sed in seed_list:
                    file.write("%s " % sed)

        print(f"\nComplete simulation, failed \033[91m{fail_num}\033[0m times / {epid} tries \n")
    else:
        print("\033[93m" + "Use Saved Seeds List".center(30, "-") + "\033[0m")
        with open(os.path.join(args["save_path"], "seed.txt"), "r") as file:
            seed_list = file.read().split()
            seed_list = [int(i) for i in seed_list]


    # command = f"cd description && bash gen_episode_instructions.sh {args['task_name']} {args['task_config']} {args['language_num']}"
    # os.system(command)


if __name__ == "__main__":
    from test_render import Sapien_TEST
    Sapien_TEST()

    import torch.multiprocessing as mp
    mp.set_start_method("spawn", force=True)

    parser = ArgumentParser()
    parser.add_argument("task_name", type=str)
    parser.add_argument("task_config", type=str)
    parser = parser.parse_args()
    task_name = parser.task_name
    task_config = parser.task_config

    main(task_name=task_name, task_config=task_config)
