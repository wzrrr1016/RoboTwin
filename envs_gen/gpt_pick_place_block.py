
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs.utils import *
import sapien

class gpt_pick_place_block(Pick_Place_Task):
    def load_actors(self):
        self.plate = self.add_actor("plate", "plate")
        
        block_pose_lst = self.create_box_pose(num=6)

        # Red blocks
        self.red_block1 = self.create_block(block_pose_lst[0], (1, 0, 0))
        self.red_block2 = self.create_block(block_pose_lst[1], (0.95, 0, 0))

        # Blue blocks
        self.blue_block1 = self.create_block(block_pose_lst[2], (0, 0, 1))
        self.blue_block2 = self.create_block(block_pose_lst[3], (0, 0, 1))
        self.blue_block3 = self.create_block(block_pose_lst[4], (0, 0, 1))

        # Green block
        self.green_block1 = self.create_block(block_pose_lst[5], (0, 1, 0))

        # Add prohibit areas
        self.add_prohibit_area(self.red_block1, padding=0.05)
        self.add_prohibit_area(self.red_block2, padding=0.05)
        self.add_prohibit_area(self.blue_block1, padding=0.05)
        self.add_prohibit_area(self.blue_block2, padding=0.05)
        self.add_prohibit_area(self.blue_block3, padding=0.05)
        self.add_prohibit_area(self.green_block1, padding=0.05)

        # Set names for identification
        self.red_block1.set_name("red_block1")
        self.red_block2.set_name("red_block2")
        self.blue_block1.set_name("blue_block1")
        self.blue_block2.set_name("blue_block2")
        self.blue_block3.set_name("blue_block3")
        self.green_block1.set_name("green_block1")
    def play_once(self):
        # Pick and place the required blocks
        success = self.pick_place_block(self.red_block1, self.plate)
        print("pick place red_block1:", success)
        if not success:
            return self.info

        success = self.pick_place_block(self.red_block2, self.plate)
        print("pick place red_block2:", success)
        if not success:
            return self.info

        success = self.pick_place_block(self.blue_block1, self.plate)
        print("pick place blue_block1:", success)
        if not success:
            return self.info

        success = self.pick_place_block(self.blue_block2, self.plate)
        print("pick place blue_block2:", success)
        if not success:
            return self.info
    def check_success(self):
        red_plate = 0
        blue_plate = 0

        # Count red blocks on the plate
        if self.check_on(self.red_block1, self.plate):
            red_plate += 1
        if self.check_on(self.red_block2, self.plate):
            red_plate += 1

        # Count blue blocks on the plate
        if self.check_on(self.blue_block1, self.plate):
            blue_plate += 1
        if self.check_on(self.blue_block2, self.plate):
            blue_plate += 1
        if self.check_on(self.blue_block3, self.plate):
            blue_plate += 1

        # Success condition: at least 2 red and 2 blue on the plate
        if red_plate >= 2 and blue_plate >= 2:
            return True
        return False
    