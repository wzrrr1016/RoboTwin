from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 153_package_handhelds_and_toys_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.mouse = self.add_actor("mouse", "mouse")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractors
        distractor_list = ["apple", "baguette", "pot-with-plant", "shoe", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Pick mouse and place into shoe_box
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Pick mouse:", success)
        if not success:
            return self.info

        # Step 2: Pick fork and place into shoe_box (wrong)
        success = self.pick_and_place(self.fork, self.shoe_box)
        print("Pick fork (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick fork from shoe_box and place on shoe_box (recovery)
        success = self.pick_and_place(self.fork, self.shoe_box)
        print("Recover fork:", success)
        if not success:
            return self.info

        # Step 4: Pick pink_block and place into shoe_box
        success = self.pick_and_place(self.pink_block, self.shoe_box)
        print("Pick pink_block:", success)
        if not success:
            return self.info

        # Step 5: Pick cup_without_handle and place on shoe_box
        success = self.pick_and_place(self.cup_without_handle, self.shoe_box)
        print("Pick cup_without_handle:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        # Check if mouse and pink_block are on the shoe_box
        return self.check_on(self.mouse, self.shoe_box) and self.check_on(self.pink_block, self.shoe_box)
