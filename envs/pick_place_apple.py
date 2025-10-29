from ._base_task import Base_Task
from ._pick_place_task import Pick_Place_Task
from .utils import *
import sapien
import math
import numpy as np


class pick_place_apple(Pick_Place_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)

    def load_actors(self):

        self.plate = rand_create_actor(
            scene=self,
            xlim=[-0.25, 0.25],
            ylim=[-0.25, 0.15],
            modelname="003_plate",
            rotate_rand=False,
            qpos=[0.5, 0.5, 0.5, 0.5],
            # scale=(0.25, 0.25, 0.25),
            convex=True,
            is_static=True,
            model_id=0,
        )

        self.add_prohibit_area(self.plate, padding=0.02)

        # self.plate = self.add_actor("plate","plate")

        self.fruit1 = rand_create_actor(
            scene=self,
            xlim=[-0.2, 0.2],
            ylim=[-0.2, -0.1],
            # rotate_lim=[0, np.pi / 6, 0],
            # qpos=[0.707225, 0.706849, -0.0100455, -0.00982061],
            # qpos=[1, 0.7, 0, 0],
            rotate_rand=True,
            modelname="035_apple",
            convex=True,
            is_static=False,
            model_id=0,
        )
        self.add_prohibit_area(self.fruit1, padding=0.02)

        self.fruit2 = rand_create_actor(
            scene=self,
            xlim=[-0.2, 0.2],
            ylim=[-0.15, -0.05],
            rotate_lim=[0, np.pi / 6, 0],
            qpos=[0.707225, 0.706849, -0.0100455, -0.00982061],
            # scale=(0.25, 0.25, 0.25),
            rotate_rand=True,
            modelname="035_apple",
            convex=True,
            model_id=0,
        )
        self.add_prohibit_area(self.fruit2, padding=0.02)

        self.fruit3 = rand_create_actor(
            scene=self,
            xlim=[-0.2, 0.2],
            ylim=[-0.05, 0.05],
            rotate_lim=[0, np.pi / 6, 0],
            # qpos=[0.707225, 0.706849, -0.0100455, -0.00982061],
            qpos=[0.5, 0.5, 0.5, 0.5],
            # scale=(0.25, 0.25, 0.25),
            rotate_rand=True,
            modelname="035_apple",
            convex=True,
            model_id=1,
        )
        self.add_prohibit_area(self.fruit3, padding=0.02)


        self.fruit1.set_name("fruit1")
        self.fruit2.set_name("fruit2")
        self.fruit3.set_name("fruit3")
        self.plate.set_name("plate")


        # self.prohibited_area.append([-0.17, -0.22, 0.17, -0.12])


    def play_once(self):
        # Initialize last gripper state
        self.save_camera_rgb("/home/wangzhuoran/RoboTwin/data/first_img.png",'front_camera')
        # print("ee pose:",self.robot.get_left_ee_pose())
        # print("fruit1 pose:",self.fruit1.get_pose().p)
        # print("fruit2 pose:",self.fruit2.get_pose().p)
        # print("fruit3 pose:",self.fruit3.get_pose().p)
        # print("plate pose:",self.plate.get_pose().p)
        self.last_gripper = None
        self.move(self.move_by_displacement(arm_tag=ArmTag("left"), z=0.1, move_axis="world"))
        # Pick and place each fruit to their target positions
        success = self.pick_and_place(self.fruit1, self.plate)
        print(self.fruit1.get_name(), " pick and place success:",success)
        if not success:
            return self.info
        success = self.pick_and_place(self.fruit2, self.plate)
        print(self.fruit2.get_name(), " pick and place success:",success)
        if not success:
            return self.info
        success = self.pick_and_place(self.fruit3, self.plate)
        print(self.fruit3.get_name(), " pick and place success:",success)
        if not success:
            return self.info

        # Store information about the fruits and which arms were used
        self.info["info"] = {
            "{A}": "fruit1",
            # "{B}": "fruit2",
            # "{C}": "fruit3",
            "{a}": str(ArmTag("left")),
            # "{b}": arm_tag2,
            # "{c}": arm_tag3,
        }
        print("play once done",self.plan_success)
        return self.info

    def check_success(self):
        print("check success")
        fruit1_pose = self.fruit1.get_pose().p
        fruit2_pose = self.fruit2.get_pose().p
        fruit3_pose = self.fruit3.get_pose().p
        target_pose = self.plate.get_pose().p
        # print("fruit1 pose:", fruit1_pose)
        # print("fruit2 pose:", fruit2_pose)
        # print("fruit3 pose:", fruit3_pose)
        # print("target pose:", target_pose)
        eps = np.array([0.08, 0.08, 0.1])

        return (np.all(abs(fruit1_pose[:3] - target_pose[:3]) < eps)
                and np.all(abs(fruit2_pose[:3] - target_pose[:3]) < eps) 
                and np.all(abs(fruit3_pose[:3] - target_pose[:3]) < eps) 
                and self.is_left_gripper_open() 
                and self.is_right_gripper_open())
        # return True
