from ._base_task import Base_Task
from ._pick_place_block_task import Pick_Place_Block_Task
from .utils import *
import sapien
import math
import numpy as np
from .utils.color import COLORS


class pick_place_block_red(Pick_Place_Block_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)

    def load_actors(self):
        print("begin load")
        
        # block_pose_lst = self.create_box_pose(num=10)

        # for i in range(10):
        #     block_pose = rand_pose(
        #         xlim=[-0.25+i*0.05,-0.25+i*0.05+0.001 ],
        #         ylim=[-0.21, -0.19],
        #         zlim=[0.741 + 0.02],
        #         qpos=[1, 0, 0, 0],
        #         ylim_prop=True,
        #         rotate_rand=True,
        #         rotate_lim=[0, 0, 0.75],
        #     )
        #     cl = COLORS['red'][i]
        #     block = self.create_block(block_pose,(cl[0]/255.0, cl[1]/255.0, cl[2]/255.0) )
        #     self.add_prohibit_area(block, padding=0.05)
        #     block.set_name(f"red_block{i+1}")
        #     setattr(self, f"red_block{i+1}", block)
        #     print("red done")

        # for i in range(10):
        #     block_pose = rand_pose(
        #         xlim=[-0.25+i*0.05,-0.25+i*0.05+0.001 ],
        #         ylim=[-0.16, -0.14],
        #         zlim=[0.741 + 0.02],
        #         qpos=[1, 0, 0, 0],
        #         ylim_prop=True,
        #         rotate_rand=True,
        #         rotate_lim=[0, 0, 0.75],
        #     )
        #     cl = COLORS['blue'][i]
        #     block = self.create_block(block_pose,(cl[0]/255.0, cl[1]/255.0, cl[2]/255.0) )
        #     self.add_prohibit_area(block, padding=0.05)
        #     block.set_name(f"blue_block{i+1}")
        #     setattr(self, f"blue_block{i+1}", block)
        #     print("blue done")

        # for i in range(10):
        #     block_pose = rand_pose(
        #         xlim=[-0.25+i*0.05,-0.25+i*0.05+0.001 ],
        #         ylim=[-0.11, -0.09],
        #         zlim=[0.741 + 0.02],
        #         qpos=[1, 0, 0, 0],
        #         ylim_prop=True,
        #         rotate_rand=True,
        #         rotate_lim=[0, 0, 0.75],
        #     )
        #     cl = COLORS['green'][i]
        #     block = self.create_block(block_pose,(cl[0]/255.0, cl[1]/255.0, cl[2]/255.0) )
        #     self.add_prohibit_area(block, padding=0.05)
        #     block.set_name(f"green_block{i+1}")
        #     setattr(self, f"green_block{i+1}", block)
        #     print("green done")

        for i in range(10):
            block_pose = rand_pose(
                xlim=[-0.25+i*0.05,-0.25+i*0.05+0.001 ],
                ylim=[-0.16, -0.14],
                zlim=[0.741 + 0.02],
                qpos=[1, 0, 0, 0],
                ylim_prop=True,
                rotate_rand=True,
                rotate_lim=[0, 0, 0.75],
            )
            cl = COLORS['yellow'][i]
            block = self.create_block(block_pose,(cl[0]/255.0, cl[1]/255.0, cl[2]/255.0) )
            self.add_prohibit_area(block, padding=0.05)
            block.set_name(f"yellow_block{i+1}")
            setattr(self, f"yellow_block{i+1}", block)
            print("yellow done")


        for i in range(10):
            block_pose = rand_pose(
                xlim=[-0.25+i*0.05,-0.25+i*0.05+0.001 ],
                ylim=[-0.01, 0.01],
                zlim=[0.741 + 0.02],
                qpos=[1, 0, 0, 0],
                ylim_prop=True,
                rotate_rand=True,
                rotate_lim=[0, 0, 0.75],
            )
            cl = COLORS['purple'][i]
            block = self.create_block(block_pose,(cl[0]/255.0, cl[1]/255.0, cl[2]/255.0) )
            self.add_prohibit_area(block, padding=0.05)
            block.set_name(f"purple_block{i+1}")
            setattr(self, f"purple_block{i+1}", block)
            print("pruple done")

        for i in range(10):
            block_pose = rand_pose(
                xlim=[-0.25+i*0.05,-0.25+i*0.05+0.001 ],
                ylim=[-0.11, -0.09],
                zlim=[0.741 + 0.02],
                qpos=[1, 0, 0, 0],
                ylim_prop=True,
                rotate_rand=True,
                rotate_lim=[0, 0, 0.75],
            )
            cl = COLORS['pink'][i]
            block = self.create_block(block_pose,(cl[0]/255.0, cl[1]/255.0, cl[2]/255.0) )
            self.add_prohibit_area(block, padding=0.05)
            block.set_name(f"pink_block{i+1}")
            setattr(self, f"pink_block{i+1}", block)
            print("pink done")

        for i in range(10):
            block_pose = rand_pose(
                xlim=[-0.25+i*0.05,-0.25+i*0.05+0.001 ],
                ylim=[-0.06, -0.04],
                zlim=[0.741 + 0.02],
                qpos=[1, 0, 0, 0],
                ylim_prop=True,
                rotate_rand=True,
                rotate_lim=[0, 0, 0.75],
            )
            cl = COLORS['orange'][i]
            block = self.create_block(block_pose,(cl[0]/255.0, cl[1]/255.0, cl[2]/255.0) )
            self.add_prohibit_area(block, padding=0.05)
            block.set_name(f"orange_block{i+1}")
            setattr(self, f"orange_block{i+1}", block)
            print("orange done")


        # for i in range(10):
        #     block_pose = rand_pose(
        #         xlim=[-0.25+i*0.05,-0.25+i*0.05+0.001 ],
        #         ylim=[-0.01, 0.01],
        #         zlim=[0.741 + 0.02],
        #         qpos=[1, 0, 0, 0],
        #         ylim_prop=True,
        #         rotate_rand=True,
        #         rotate_lim=[0, 0, 0.75],
        #     )
        #     cl = COLORS['grey'][i]
        #     block = self.create_block(block_pose,(cl[0]/255.0, cl[1]/255.0, cl[2]/255.0) )
        #     self.add_prohibit_area(block, padding=0.05)
        #     block.set_name(f"grey_block{i+1}")
        #     setattr(self, f"grey_block{i+1}", block)
        #     print("grey done")


    def play_once(self):

        self.save_camera_rgb("/home/wangzhuoran/RoboTwin/data/first_img.png",'front_camera')
        # success = self.pick_place_block(self.red_block1,self.plate)
        # print("pick place red_block1:",success)
        # if not success:
        #     return self.info
        # success = self.pick_place_block(self.red_block2,self.plate)
        # print("pick place red_block2:",success)
        # if not success:
        #     return self.info
        # success = self.pick_place_block(self.blue_block1,self.plate)
        # print("pick place blue_block1:",success)
        # if not success:
        #     return self.info
        
        # success = self.pick_place_block(self.green_block1,self.plate)
        # print("pick place green_block1:",success)
        # if not success:
        #     return self.info

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
        
        # if self.check_on(self.red_block1, self.plate) and self.check_on(self.red_block2, self.plate) and self.check_on(self.blue_block1, self.plate) and self.check_on(self.green_block1, self.plate):
        #     return True
        # return False
        return True
