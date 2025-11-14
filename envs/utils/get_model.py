import random
from .color import COLORS
from .asset_list import *
from .rand_create_actor import *

def get_modelname(actor_name):
    if actor_name in asset_models.keys():
        modelname = asset_models[actor_name]["model"]
        model_type = asset_models[actor_name].get("type","other")
        scale = asset_models[actor_name].get("scale",(1.0,1.0,1.0))
        model_extents = asset_models[actor_name].get("extents",(0.1,0.1,0.1))
        model_size = np.array(model_extents)*np.array(scale)
        model_radius = max(np.linalg.norm(model_size[:2])/2.0, np.linalg.norm(model_size[1:])/2.0, np.linalg.norm(model_size[::2])/2.0)
        if model_type != "container":
            scale = (scale[0]*0.96,scale[1]*0.96,scale[2]*0.96)
        return modelname, model_type, scale, model_radius
    else:
        # print(f"Error: {actor_name} not in asset list")
        return None, None, (1.0,1.0,1.0), 0.05

def get_model_id(actor_name):
    if actor_name in asset_models.keys():
        idx_list = asset_models[actor_name]["idx"]
        model_id = random.choice(idx_list)
        return model_id
    else:
        # print(f"Error: {actor_name} not in asset list")
        return None
    
def get_grasp_type(actor_name):
    if actor_name in predict_grasp_list:
        return "predict"
    else:
        return "point"
    
def get_args_from_modeltype(model_type,object_pose=None, radius=0.05, prohibited_area=None,xlim=[-0.28,0.28],ylim=[-0.20,0.10],zlim=[0.741]):
    if model_type == "object":
        rotate_lim = [1, 1, 1]
        rotate_rand = True
        qpos = [1, 0, 0, 0]
        is_static = False
        convex = True
    elif model_type == "object_flat":
        rotate_lim = [0, 1, 0]
        rotate_rand = True
        qpos = [0.5, 0.5, 0.5, 0.5]
        is_static = False
        convex = True
    elif model_type == "object_down":
        rotate_lim = [0, 1, 0]
        rotate_rand = True
        qpos = [0, 1, 0, 0]
        is_static = False
        convex = True
    elif model_type == "pen":
        rotate_lim = [0, 1, 0]
        rotate_rand = True
        qpos = [1, 0, 0, 0]
        is_static = True
        convex = True
    elif model_type == "tool":
        rotate_lim = [0, 1, 0]
        rotate_rand = False
        qpos = [0, 0, 0.995, 0.105]
        is_static = True
        convex = True
        zlim = [0.76]
    elif model_type == "container":
        rotate_lim = [0, 1, 0]
        rotate_rand = True
        qpos = [0.5, 0.5, 0.5, 0.5]
        is_static = True
        convex = False
    elif model_type == "bottle":
        rotate_lim = [0, 1, 0]
        rotate_rand = True
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            qpos = [0.66, 0.66, -0.25, -0.25]
            xlim = [-0.28, 0]
        else:
            qpos = [0.66, 0.66, 0.25, 0.25]
            xlim = [0, 0.28]
        is_static = False
        convex = True
    else: # other
        rotate_lim = [0, 0, 0]
        rotate_rand = False
        qpos = [1, 0, 0, 0]
        is_static = False
        convex = True

    if object_pose is None:
        object_pose = rand_pose(
                    xlim=xlim,
                    ylim=ylim,
                    zlim=zlim,
                    rotate_rand=rotate_rand,
                    rotate_lim=rotate_lim,
                    qpos=qpos,
                    radius=radius,
                    prohibit_area=prohibited_area,
                )

    return object_pose, is_static, convex

def get_color(color):
    if color in COLORS:
        cl_list = COLORS[color]
        cl = random.choice(cl_list)
        return (cl[0]/255.0,cl[1]/255.0,cl[2]/255.0)
    
def get_color_from_name(object_name):
    for color in COLORS.keys():
        if color in object_name.lower():
            return color
    return "grey"