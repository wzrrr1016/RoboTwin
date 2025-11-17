from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 191_store_drinkware_and_toys_correction(Imagine_Task):
    def load_actors(self):
        # Add the shoe_box as a container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        # Add drinkware (cups)
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        # Add small non-perishable play item (orange_block)
        self.orange_block = self.add_actor("orange_block", "orange_block")
        # Add apple (perishable, should not be in the box)
        self.apple = self.add_actor("apple", "apple")
        # Add distractors
        distractor_list = ['calculator', 'screwdriver', 'book', 'small-speaker']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place cup_with_handle into shoe_box
        success = self.pick_and_place(self.cup_with_handle, self.shoe_box)
        print("Place cup_with_handle:", success)
        if not success:
            return self.info

        # Step 2: Place apple into shoe_box (wrong)
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Place apple (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover apple to orange_block
        success = self.pick_and_place(self.apple, self.orange_block)
        print("Recover apple to orange_block:", success)
        if not success:
            return self.info

        # Step 4: Place orange_block into shoe_box
        success = self.pick_and_place(self.orange_block, self.shoe_box)
        print("Place orange_block into shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place cup_without_handle into shoe_box
        success = self.pick_and_place(self.cup_without_handle, self.shoe_box)
        print("Place cup_without_handle:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all correct items are in the shoe_box and apple is not
        if (self.check_on(self.cup_with_handle, self.shoe_box) and
            self.check_on(self.cup_without_handle, self.shoe_box) and
            self.check_on(self.orange_block, self.shoe_box) and
            not self.check_on(self.apple, self.shoe_box)):
            return True
        return False
