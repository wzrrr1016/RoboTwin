from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 48_perishable_and_hazard_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.knife = self.add_actor("knife", "knife")
        self.scanner = self.add_actor("scanner", "scanner")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add distractors
        distractor_list = ['pot-with-plant', 'sand-clock', 'book', 'shoe', 'purple_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place edible items on plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Place apple on plate:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french fries on plate:", success)
        if not success:
            return self.info
        
        # Place non-edible/hazardous items in dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Place knife in dustbin:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.scanner, self.dustbin)
        print("Place scanner in dustbin:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Place bottle in dustbin:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Verify edible items are on plate
        if not self.check_on(self.apple, self.plate):
            return False
        if not self.check_on(self.french_fries, self.plate):
            return False
        
        # Verify non-edible items are in dustbin
        if not self.check_on(self.knife, self.dustbin):
            return False
        if not self.check_on(self.scanner, self.dustbin):
            return False
        if not self.check_on(self.bottle, self.dustbin):
            return False
        
        return True
