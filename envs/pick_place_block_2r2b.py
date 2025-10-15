
from envs._base_task import Base_Task
from envs._pick_place_block_task import Pick_Place_Block_Task
from envs.utils import *
import sapien

class pick_place_block_2r2b(Pick_Place_Block_Task):
    def load_actors(self):
        self.plate = self.add_actor("plate", "plate")
        
        block_pose_lst = self.create_box_pose(num=6)

        # Two red blocks
        self.red_block1 = self.create_block(block_pose_lst[0], 'red')
        self.red_block2 = self.create_block(block_pose_lst[1], 'red')

        # Three blue blocks
        self.blue_block1 = self.create_block(block_pose_lst[2], 'blue')
        self.blue_block2 = self.create_block(block_pose_lst[3], 'blue')
        self.blue_block3 = self.create_block(block_pose_lst[4], 'blue')

        # One green block
        self.green_block1 = self.create_block(block_pose_lst[5], 'green')

        # Add prohibit areas
        self.add_prohibit_area(self.red_block1, padding=0.05)
        self.add_prohibit_area(self.red_block2, padding=0.05)
        self.add_prohibit_area(self.blue_block1, padding=0.05)
        self.add_prohibit_area(self.blue_block2, padding=0.05)
        self.add_prohibit_area(self.blue_block3, padding=0.05)
        self.add_prohibit_area(self.green_block1, padding=0.05)

        # Set names for clarity
        self.red_block1.set_name("red_block1")
        self.red_block2.set_name("red_block2")
        self.blue_block1.set_name("blue_block1")
        self.blue_block2.set_name("blue_block2")
        self.blue_block3.set_name("blue_block3")
        self.green_block1.set_name("green_block1")
    def play_once(self):
        # Pick and place two red blocks
        success = self.pick_place_block(self.red_block1, self.plate)
        print("pick place red_block1:", success)
        if not success:
            return self.info
        success = self.pick_place_block(self.red_block2, self.plate)
        print("pick place red_block2:", success)
        if not success:
            return self.info

        # Pick and place two blue blocks
        success = self.pick_place_block(self.blue_block1, self.plate)
        print("pick place blue_block1:", success)
        if not success:
            return self.info
        success = self.pick_place_block(self.blue_block2, self.plate)
        print("pick place blue_block2:", success)
        if not success:
            return self.info
    def check_success(self):
        red_on_plate = 0
        blue_on_plate = 0

        # Count red blocks on the plate
        if self.check_on(self.red_block1, self.plate):
            red_on_plate += 1
        if self.check_on(self.red_block2, self.plate):
            red_on_plate += 1

        # Count blue blocks on the plate
        if self.check_on(self.blue_block1, self.plate):
            blue_on_plate += 1
        if self.check_on(self.blue_block2, self.plate):
            blue_on_plate += 1
        if self.check_on(self.blue_block3, self.plate):
            blue_on_plate += 1

        # Check if at least 2 red and 2 blue blocks are on the plate
        if red_on_plate >= 2 and blue_on_plate >= 2:
            return True
        return False
    