from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 44_store_handled_drinkware_and_dispose_small_items_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add required objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.mug = self.add_actor("mug", "mug")
        self.stapler = self.add_actor("stapler", "stapler")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        
        # Add distractors
        distractor_list = ['pot-with-plant', 'alarm-clock', 'microphone', 'dumbbell', 'baguette']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Put cup_with_handle into shoe_box
        success = self.pick_and_place(self.cup_with_handle, self.shoe_box)
        print("Put cup_with_handle into shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Wrongly put mug into dustbin
        success = self.pick_and_place(self.mug, self.dustbin)
        print("Put mug into dustbin (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recovery - Put mug into shoe_box
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Recover mug into shoe_box:", success)
        if not success:
            return self.info

        # Step 4: Put stapler into dustbin
        success = self.pick_and_place(self.stapler, self.dustbin)
        print("Put stapler into dustbin:", success)
        if not success:
            return self.info

        # Step 5: Put orange_block into dustbin
        success = self.pick_and_place(self.orange_block, self.dustbin)
        print("Put orange_block into dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all objects are in their correct final positions
        if (self.check_on(self.cup_with_handle, self.shoe_box) and
            self.check_on(self.mug, self.shoe_box) and
            self.check_on(self.stapler, self.dustbin) and
            self.check_on(self.orange_block, self.dustbin)):
            return True
        return False
