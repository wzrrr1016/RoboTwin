from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 62_place_edible_and_tools_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add target objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.stapler = self.add_actor("stapler", "stapler")
        
        # Add distractors
        distractor_list = ["pot-with-plant", "shoe", "book", "alarm-clock", "toycar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # First wrong action: Place screwdriver on plate
        success = self.pick_and_place(self.screwdriver, self.plate)
        print("Pick screwdriver and place on plate:", success)
        if not success:
            return self.info
        
        # Recovery: Move screwdriver to fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Pick screwdriver from plate and place in fluted_block:", success)
        if not success:
            return self.info
        
        # Place stapler in fluted_block
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Pick stapler and place in fluted_block:", success)
        if not success:
            return self.info
        
        # Place apple on plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Pick apple and place on plate:", success)
        if not success:
            return self.info
        
        # Place bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Pick bread and place on plate:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct final positions
        if (self.check_on(self.apple, self.plate) and
            self.check_on(self.bread, self.plate) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.stapler, self.fluted_block)):
            return True
        return False
