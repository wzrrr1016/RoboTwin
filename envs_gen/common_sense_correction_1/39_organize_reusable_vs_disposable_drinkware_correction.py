from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 39_organize_reusable_vs_disposable_drinkware_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Create target objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        
        # Add distractors
        self.add_distractors(["calculator", "toycar", "book", "shoe", "markpen"])

    def play_once(self):
        # Place bottle in organizer (fluted_block)
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Bottle placement:", success)
        if not success:
            return self.info
            
        # Place can in dustbin (not fluted_block)
        success = self.pick_and_place(self.can, self.dustbin)
        print("Can placement:", success)
        if not success:
            return self.info
            
        # Place cup_with_handle in organizer
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Cup with handle placement:", success)
        if not success:
            return self.info
            
        # Place cup_without_handle in dustbin
        success = self.pick_and_place(self.cup_without_handle, self.dustbin)
        print("Cup without handle placement:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.cup_without_handle, self.dustbin)):
            return True
        return False
