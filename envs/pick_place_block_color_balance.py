
from envs._base_task import Base_Task
from envs._pick_place_block_task import Pick_Place_Block_Task
from envs.utils import *
import sapien

class pick_place_block_color_balance(Pick_Place_Block_Task):
    def load_actors(self):
        # Add the green bowl
        self.bowl = self.add_actor("bowl", "bowl")
        self.bowl.set_name("bowl")

        # Create 7 block poses
        block_pose_lst = self.create_box_pose(num=7)

        # Create the blocks
        self.red_block1 = self.create_block(block_pose_lst[0], "red")
        self.red_block2 = self.create_block(block_pose_lst[1], "red")
        self.red_block3 = self.create_block(block_pose_lst[2], "red")
        self.blue_block1 = self.create_block(block_pose_lst[3], "blue")
        self.blue_block2 = self.create_block(block_pose_lst[4], "blue")
        self.yellow_block = self.create_block(block_pose_lst[5], "yellow")
        self.green_block = self.create_block(block_pose_lst[6], "green")

        # Add prohibit areas
        self.add_prohibit_area(self.red_block1, padding=0.05)
        self.add_prohibit_area(self.red_block2, padding=0.05)
        self.add_prohibit_area(self.red_block3, padding=0.05)
        self.add_prohibit_area(self.blue_block1, padding=0.05)
        self.add_prohibit_area(self.blue_block2, padding=0.05)
        self.add_prohibit_area(self.yellow_block, padding=0.05)
        self.add_prohibit_area(self.green_block, padding=0.05)

        # Set names
        self.red_block1.set_name("red_block1")
        self.red_block2.set_name("red_block2")
        self.red_block3.set_name("red_block3")
        self.blue_block1.set_name("blue_block1")
        self.blue_block2.set_name("blue_block2")
        self.yellow_block.set_name("yellow_block")
        self.green_block.set_name("green_block")
    def play_once(self):
        # Move 1 red block to the bowl
        success = self.pick_place_block(self.red_block1, self.bowl)
        print("pick place red_block1:", success)
        if not success:
            return self.info

        # Move both blue blocks to the bowl
        success = self.pick_place_block(self.blue_block1, self.bowl)
        print("pick place blue_block1:", success)
        if not success:
            return self.info

        success = self.pick_place_block(self.blue_block2, self.bowl)
        print("pick place blue_block2:", success)
        if not success:
            return self.info
    def check_success(self):
        # Check that both blue blocks are in the bowl
        if not (self.check_on(self.blue_block1, self.bowl) and self.check_on(self.blue_block2, self.bowl)):
            return False

        # Check that exactly one red block is in the bowl
        red_in_bowl = 0
        if self.check_on(self.red_block1, self.bowl):
            red_in_bowl += 1
        if self.check_on(self.red_block2, self.bowl):
            red_in_bowl += 1
        if self.check_on(self.red_block3, self.bowl):
            red_in_bowl += 1

        if red_in_bowl != 1:
            return False

        # Check that the total number of blocks in the bowl is 3 (odd)
        total_in_bowl = 2 + red_in_bowl
        if total_in_bowl != 3:
            return False

        # Check that the number of red blocks on the table equals the number of blue blocks in the bowl
        red_on_table = 3 - red_in_bowl
        blue_in_bowl = 2
        if red_on_table != blue_in_bowl:
            return False

        return True
    