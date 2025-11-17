from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 89_stable_support_and_perishable_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractors
        distractor_list = ["calculator", "alarm-clock", "toycar", "markpen", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Initial wrong placement of bottle into wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Pick bottle into wooden_box (wrong):", success)
        if not success:
            return self.info
        
        # Step 2: Recovery - move bottle to fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Recover bottle to fluted_block:", success)
        if not success:
            return self.info
        
        # Step 3: Place cup_with_handle onto fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Place cup_with_handle:", success)
        if not success:
            return self.info
        
        # Step 4: Place dumbbell onto fluted_block
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        print("Place dumbbell:", success)
        if not success:
            return self.info
        
        # Step 5: Place bread into wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Place bread:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all required objects are in their correct containers
        if (self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.dumbbell, self.fluted_block) and
            self.check_on(self.bread, self.wooden_box)):
            return True
        return False
