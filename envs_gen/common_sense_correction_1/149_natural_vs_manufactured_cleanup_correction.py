from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 149_natural_vs_manufactured_cleanup_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Add objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.apple = self.add_actor("apple", "apple")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        # Add distractors
        distractor_list = ['microphone', 'alarm-clock', 'sand-clock', 'small-speaker']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place red_block into dustbin
        success = self.pick_and_place(self.red_block, self.dustbin)
        print("Place red_block into dustbin:", success)
        if not success:
            return self.info

        # Wrongly place apple into dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Wrongly place apple into dustbin:", success)
        if not success:
            return self.info

        # Recover apple to coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Recover apple to coaster:", success)
        if not success:
            return self.info

        # Place pot-with-plant onto coaster
        success = self.pick_and_place(self.pot_with_plant, self.coaster)
        print("Place pot-with-plant onto coaster:", success)
        if not success:
            return self.info

        # Place orange_block into dustbin
        success = self.pick_and_place(self.orange_block, self.dustbin)
        print("Place orange_block into dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all required objects are in the correct locations
        red_in_dustbin = self.check_on(self.red_block, self.dustbin)
        orange_in_dustbin = self.check_on(self.orange_block, self.dustbin)
        apple_on_coaster = self.check_on(self.apple, self.coaster)
        pot_on_coaster = self.check_on(self.pot_with_plant, self.coaster)

        return red_in_dustbin and orange_in_dustbin and apple_on_coaster and pot_on_coaster
