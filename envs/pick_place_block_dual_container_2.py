
from envs._base_task import Base_Task
from envs._pick_place_block_task import Pick_Place_Block_Task
from envs.utils import *
import sapien

class pick_place_block_dual_container_2(Pick_Place_Block_Task):
    def load_actors(self):
        # Add the plate and black bowl to the environment
        self.plate = self.add_actor("plate", "plate")
        self.black_bowl = self.add_actor("bowl", "black_bowl")

        # Create 4 block poses
        block_pose_lst = self.create_box_pose(num=4)

        # Create the blocks with the correct colors
        self.orange_block1 = self.create_block(block_pose_lst[0], "orange")
        self.orange_block2 = self.create_block(block_pose_lst[1], "orange")
        self.pink_block = self.create_block(block_pose_lst[2], "pink")
        self.purple_block = self.create_block(block_pose_lst[3], "purple")

        # Add prohibit areas to avoid collisions
        self.add_prohibit_area(self.orange_block1, padding=0.05)
        self.add_prohibit_area(self.orange_block2, padding=0.05)
        self.add_prohibit_area(self.pink_block, padding=0.05)
        self.add_prohibit_area(self.purple_block, padding=0.05)

        # Set names for easier reference
        self.orange_block1.set_name("orange_block1")
        self.orange_block2.set_name("orange_block2")
        self.pink_block.set_name("pink_block")
        self.purple_block.set_name("purple_block")
    def play_once(self):
        # Place both orange blocks into the black bowl
        success = self.pick_place_block(self.orange_block1, self.black_bowl)
        print("pick place orange_block1:", success)
        if not success:
            return self.info

        success = self.pick_place_block(self.orange_block2, self.black_bowl)
        print("pick place orange_block2:", success)
        if not success:
            return self.info

        # Place the pink and purple blocks on the plate
        success = self.pick_place_block(self.pink_block, self.plate)
        print("pick place pink_block:", success)
        if not success:
            return self.info

        success = self.pick_place_block(self.purple_block, self.plate)
        print("pick place purple_block:", success)
        if not success:
            return self.info
    def check_success(self):
        # Check if both orange blocks are on the black bowl
        if self.check_on(self.orange_block1, self.black_bowl) and self.check_on(self.orange_block2, self.black_bowl):
            # Check if pink and purple blocks are on the plate
            if self.check_on(self.pink_block, self.plate) and self.check_on(self.purple_block, self.plate):
                return True
        return False
    