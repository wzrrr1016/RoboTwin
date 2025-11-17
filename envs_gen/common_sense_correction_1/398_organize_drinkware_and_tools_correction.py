from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 398_organize_drinkware_and_tools_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.hammer = self.add_actor("hammer", "hammer")
        self.stapler = self.add_actor("stapler", "stapler")
        
        # Add distractors
        distractor_list = ["apple", "baguette", "hamburg", "french_fries", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place mug on coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Place mug on coaster:", success)
        if not success:
            return self.info
            
        # Place cup without handle on coaster
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Place cup without handle on coaster:", success)
        if not success:
            return self.info
            
        # Place stapler on coaster (wrong placement)
        success = self.pick_and_place(self.stapler, self.coaster)
        print("Place stapler on coaster (wrong):", success)
        if not success:
            return self.info
            
        # Recover by moving stapler to fluted_block
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Move stapler to fluted_block:", success)
        if not success:
            return self.info
            
        # Place hammer on fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Place hammer on fluted_block:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Verify all required placements
        if (self.check_on(self.mug, self.coaster) and
            self.check_on(self.cup_without_handle, self.coaster) and
            self.check_on(self.stapler, self.fluted_block) and
            self.check_on(self.hammer, self.fluted_block)):
            return True
        return False
