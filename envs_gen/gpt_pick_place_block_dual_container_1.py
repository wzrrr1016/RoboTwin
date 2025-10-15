
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs.utils import *
import sapien

class gpt_pick_place_block_dual_container_1(Pick_Place_Task):
    def load_actors(self):
        # Add the green and yellow bowls
        self.green_bowl = self.add_actor("bowl", "green_bowl")
        self.yellow_bowl = self.add_actor("bowl", "yellow_bowl")

        # Create box poses for the blocks
        block_pose_lst = self.create_box_pose(num=5)

        # Create the blocks
        self.red_block = self.create_block(block_pose_lst[0], "red")
        self.green_block = self.create_block(block_pose_lst[1], "green")
        self.blue_block = self.create_block(block_pose_lst[2], "blue")
        self.yellow_block = self.create_block(block_pose_lst[3], "yellow")
        self.purple_block = self.create_block(block_pose_lst[4], "purple")

        # Add prohibit areas for all blocks
        self.add_prohibit_area(self.red_block, padding=0.05)
        self.add_prohibit_area(self.green_block, padding=0.05)
        self.add_prohibit_area(self.blue_block, padding=0.05)
        self.add_prohibit_area(self.yellow_block, padding=0.05)
        self.add_prohibit_area(self.purple_block, padding=0.05)

        # Set names for the blocks
        self.red_block.set_name("red_block")
        self.green_block.set_name("green_block")
        self.blue_block.set_name("blue_block")
        self.yellow_block.set_name("yellow_block")
        self.purple_block.set_name("purple_block")
    def play_once(self):
        # Place red block in green bowl
        success = self.pick_place_block(self.red_block, self.green_bowl)
        print("pick place red_block:", success)
        if not success:
            return self.info

        # Place blue block in green bowl
        success = self.pick_place_block(self.blue_block, self.green_bowl)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        # Place green block in yellow bowl
        success = self.pick_place_block(self.green_block, self.yellow_bowl)
        print("pick place green_block:", success)
        if not success:
            return self.info

        # Place yellow block in yellow bowl
        success = self.pick_place_block(self.yellow_block, self.yellow_bowl)
        print("pick place yellow_block:", success)
        if not success:
            return self.info
    def check_success(self):
        # Check green bowl has red and blue
        green_bowl_has_red = self.check_on(self.red_block, self.green_bowl)
        green_bowl_has_blue = self.check_on(self.blue_block, self.green_bowl)
        # Check yellow bowl has green and yellow
        yellow_bowl_has_green = self.check_on(self.green_block, self.yellow_bowl)
        yellow_bowl_has_yellow = self.check_on(self.yellow_block, self.yellow_bowl)
        return green_bowl_has_red and green_bowl_has_blue and yellow_bowl_has_green and yellow_bowl_has_yellow
    