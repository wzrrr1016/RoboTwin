from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 321_liquids_on_block_heavy_in_box_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add required objects
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.hammer = self.add_actor("hammer", "hammer")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add distractors
        distractor_list = ["calculator", "toycar", "shoe", "book", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Initial wrong action: place bottle in shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("Place bottle into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Recovery: move bottle to fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Recover: Place bottle onto fluted_block:", success)
        if not success:
            return self.info

        # Place shampoo on fluted_block
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Place shampoo:", success)
        if not success:
            return self.info

        # Place hammer in shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Place hammer:", success)
        if not success:
            return self.info

        # Place dumbbell in shoe_box
        success = self.pick_and_place(self.dumbbell, self.shoe_box)
        print("Place dumbbell:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all items are in their correct locations
        if (self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.shampoo, self.fluted_block) and
            self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.dumbbell, self.shoe_box)):
            return True
        return False
