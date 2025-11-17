from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 21_place_dry_small_items_on_coaster_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add the objects to be manipulated
        self.green_block = self.add_actor("green_block", "green_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractors to the environment
        distractor_list = ["pot-with-plant", "dumbbell", "shoe", "microphone", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: Place french_fries on coaster (incorrect item)
        success = self.pick_and_place(self.french_fries, self.coaster)
        print("Wrong action - Place french_fries on coaster:", success)
        if not success:
            return self.info

        # Recovery: Place french_fries back on the table
        success = self.pick_and_place(self.french_fries, self.table)
        print("Recovery - Place french_fries on table:", success)
        if not success:
            return self.info

        # Place correct items on the coaster
        success = self.pick_and_place(self.green_block, self.coaster)
        print("Place green_block on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.coaster)
        print("Place blue_block on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all correct items are on the coaster
        correct_items_on_coaster = (
            self.check_on(self.green_block, self.coaster) and
            self.check_on(self.blue_block, self.coaster) and
            self.check_on(self.apple, self.coaster)
        )
        
        # Ensure the incorrect item (french_fries) is not on the coaster
        incorrect_item_not_on_coaster = not self.check_on(self.french_fries, self.coaster)
        
        return correct_items_on_coaster and incorrect_item_not_on_coaster
