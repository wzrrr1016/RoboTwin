from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 360_organize_food_drinkware_and_toys_with_recycle_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.can = self.add_actor("can", "can")
        
        # Add distractors
        distractor_list = ["screwdriver", "shoe", "book", "alarm-clock", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place apple on fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple:", success)
        if not success:
            return self.info

        # Wrong placement: can on fluted_block
        success = self.pick_and_place(self.can, self.fluted_block)
        print("Wrong placement can:", success)
        if not success:
            return self.info

        # Recovery: move can to dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Recover can:", success)
        if not success:
            return self.info

        # Place cup_with_handle on fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Place cup_with_handle:", success)
        if not success:
            return self.info

        # Place red_block on fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info

        # Place green_block on fluted_block
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        if (
            self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.green_block, self.fluted_block) and
            self.check_on(self.can, self.dustbin)
        ):
            return True
        return False
