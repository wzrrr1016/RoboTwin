from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 4_square_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.green_block = self.add_actor("green_block", "green_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.mouse = self.add_actor("mouse", "mouse")

        # Add distractors
        distractor_list = ["apple", "bread", "toycar", "pot-with-plant", "book", "msg"]
        self.add_distractors(distractor_list)

        self.check_scene()

    def play_once(self):
        # Place solid square blocks into coaster
        for block in [self.green_block, self.yellow_block, self.purple_block]:
            success = self.pick_and_place(block, self.coaster)
            print(f"Place {block} into coaster: {success}")
            if not success:
                return self.info

        # Place shampoo into coaster (wrong action)
        success = self.pick_and_place(self.shampoo, self.coaster)
        print(f"Place shampoo into coaster (wrong): {success}")
        if not success:
            return self.info

        # Recovery: move shampoo to dustbin
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print(f"Place shampoo into dustbin (recovery): {success}")
        if not success:
            return self.info

        # Place mouse into dustbin
        success = self.pick_and_place(self.mouse, self.dustbin)
        print(f"Place mouse into dustbin: {success}")
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        # Check if all blocks are on coaster
        blocks_on_coaster = all(self.check_on(block, self.coaster) for block in 
                               [self.green_block, self.yellow_block, self.purple_block])
        
        # Check if shampoo and mouse are on dustbin
        shampoo_on_dustbin = self.check_on(self.shampoo, self.dustbin)
        mouse_on_dustbin = self.check_on(self.mouse, self.dustbin)
        
        return blocks_on_coaster and shampoo_on_dustbin and mouse_on_dustbin
