import random
from .color import COLORS
from .asset_list import *


def get_modelname(actor_name):
    if actor_name in asset_models.keys():
        modelname = asset_models[actor_name]["model"]
        if actor_name in objects_able_to_pick_list:
            return modelname, "object"
        elif actor_name in containers_list:
            return modelname, "container"
        elif actor_name in bottle_list:
            return modelname, "bottle"
        else:
            return modelname, "other"
    else:
        print(f"Error: {actor_name} not in asset list")
        return None, None

def get_model_id(actor_name):
    if actor_name in asset_models.keys():
        num = asset_models[actor_name]["num"]
        model_id = random.randint(0, num-1)
        return model_id
    else:
        print(f"Error: {actor_name} not in asset list")
        return None
    
def get_args_from_modeltype(model_type,model_name,model_id):
    scale = (1,1,1)
    if model_type == "object":
        rotate_lim = [1, 1, 1]
        rotate_rand = True
        qpos = [1, 0, 0, 0]
        is_static = False
        convex = False
    elif model_type == "container":
        rotate_lim = [0, 1, 0]
        rotate_rand = True
        qpos = [0.5, 0.5, 0.5, 0.5]
        is_static = True
        convex = True
    elif model_type == "bottle":
        rotate_lim = [0, 1, 0]
        rotate_rand = True
        qpos = [0.66, 0.66, -0.25, -0.25]
        is_static = False
        convex = True
        scale = (0.8,0.8,0.8)
    else: # other
        rotate_lim = [0, 0, 0]
        rotate_rand = False
        qpos = [1, 0, 0, 0]
        is_static = True
        convex = False
    if model_name in special_object_args.keys():
        args = special_object_args[model_name]
        if "scale" in args.keys():
            scale = args["scale"]
    return rotate_lim, rotate_rand, qpos, is_static, convex, scale

def get_color(color):
    if color in COLORS:
        cl_list = COLORS[color]
        cl = random.choice(cl_list)
        return (cl[0]/255.0,cl[1]/255.0,cl[2]/255.0)