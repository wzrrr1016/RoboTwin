from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 40_unhealthy_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add all objects to the environment
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.green_block = self.add_actor("green_block", "green_block")
        self.mug = self.add_actor("mug", "mug")
        self.hamburg = self.add_actor("hamburg", "hamburg")

    def play_once(self):
        # Step 1: Pick hamburg and place into wooden_box
        success = self.pick_and_place(self.hamburg, self.wooden_box)
        print("Pick hamburg into wooden_box:", success)
        if not success:
            return self.info

        # Step 2: Pick mug and place into wooden_box (wrong)
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Pick mug into wooden_box:", success)
        if not success:
            return self.info

        # Step 3: Pick mug from wooden_box and place into shoe_box (recovery)
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Pick mug from wooden_box to shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if hamburg is in wooden_box
        if not self.check_on(self.hamburg, self.wooden_box):
            return False

        # Check if mug is in shoe_box
        if not self.check_on(self.mug, self.shoe_box):
            return False

        # Assume other items (blue_block, cup_without_handle, green_block) are already in shoe_box
        return True
