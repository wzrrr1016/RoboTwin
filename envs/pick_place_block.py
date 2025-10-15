from ._base_task import Base_Task
from ._pick_place_block_task import Pick_Place_Block_Task
from .utils import *
import sapien
import math
import numpy as np


class pick_place_block(Pick_Place_Block_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)

    def load_actors(self):
        print("begin load")

        self.plate = self.add_actor("plate","plate")
        
        block_pose_lst = self.create_box_pose(num=6)

        self.red_block1 = self.create_block(block_pose_lst[0], "red")
        self.red_block2 = self.create_block(block_pose_lst[1], "red")
        self.green_block1 = self.create_block(block_pose_lst[2], "green")
        self.green_block2 = self.create_block(block_pose_lst[3], "green")
        self.blue_block1 = self.create_block(block_pose_lst[4], "blue")
        self.blue_block2 = self.create_block(block_pose_lst[5], "blue")

        self.add_prohibit_area(self.red_block1, padding=0.05)
        self.add_prohibit_area(self.red_block2, padding=0.05)
        self.add_prohibit_area(self.blue_block1, padding=0.05)
        self.add_prohibit_area(self.blue_block2, padding=0.05)
        self.add_prohibit_area(self.green_block1, padding=0.05)
        self.add_prohibit_area(self.green_block2, padding=0.05)


        self.red_block1.set_name("red_block1")
        self.red_block2.set_name("red_block2")
        self.blue_block1.set_name("blue_block1")
        self.blue_block2.set_name("blue_block2")
        self.green_block1.set_name("green_block1")
        self.green_block2.set_name("green_block2")

        print("load actor success")

    def play_once(self):

        self.save_camera_rgb("/home/wangzhuoran/RoboTwin/data/first_img.png",'front_camera')
        success = self.pick_place_block(self.red_block1,self.plate)
        print("pick place red_block1:",success)
        if not success:
            return self.info
        success = self.pick_place_block(self.red_block2,self.plate)
        print("pick place red_block2:",success)
        if not success:
            return self.info
        success = self.pick_place_block(self.blue_block1,self.plate)
        print("pick place blue_block1:",success)
        if not success:
            return self.info
        
        success = self.pick_place_block(self.green_block1,self.plate)
        print("pick place green_block1:",success)
        if not success:
            return self.info

        # Store information about the blocks and which arms were used
        self.info["info"] = {
            "{A}": "block1",
            # "{B}": "block2",
            # "{C}": "block3",
            "{a}": str(ArmTag("left")),
            # "{b}": arm_tag2,
            # "{c}": arm_tag3,
        }
        print("play once done",self.plan_success)
        return self.info
    

    def check_success(self):
        
        if self.check_on(self.red_block1, self.plate) and self.check_on(self.red_block2, self.plate) and self.check_on(self.blue_block1, self.plate) and self.check_on(self.green_block1, self.plate):
            return True
        return False
