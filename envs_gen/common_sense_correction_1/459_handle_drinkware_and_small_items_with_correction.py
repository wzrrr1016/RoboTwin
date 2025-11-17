from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 459_handle_drinkware_and_small_items_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.mug = self.add_actor("mug", "mug")
        self.stapler = self.add_actor("stapler", "stapler")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractors
        distractor_list = ["baguette", "apple", "book", "red_block", "blue_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Wrong placement of small_speaker into wooden_box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Place small_speaker into wooden_box (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery, move small_speaker to shoe_box
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Recover small_speaker to shoe_box:", success)
        if not success:
            return self.info

        # Step 3: Place mug into wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Place mug into wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place cup_with_handle into wooden_box
        success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
        print("Place cup_with_handle into wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Place stapler into shoe_box
        success = self.pick_and_place(self.stapler, self.shoe_box)
        print("Place stapler into shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        if (self.check_on(self.cup_with_handle, self.wooden_box) and
            self.check_on(self.mug, self.wooden_box) and
            self.check_on(self.stapler, self.shoe_box) and
            self.check_on(self.small_speaker, self.shoe_box)):
            return True
        return False
