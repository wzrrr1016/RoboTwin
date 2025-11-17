from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 488_organize_tools_and_dispose_food_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add objects
        self.drill = self.add_actor("drill", "drill")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.stapler = self.add_actor("stapler", "stapler")
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractors
        distractor_list = ["pet-collar", "toycar", "pot-with-plant", "alarm-clock", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Pick and place drill on fluted_block
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Pick drill:", success)
        if not success:
            return self.info
        
        # Pick and place screwdriver on fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Pick screwdriver:", success)
        if not success:
            return self.info
        
        # Wrong placement of french_fries on fluted_block
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Pick french_fries (wrong):", success)
        if not success:
            return self.info
        
        # Recovery: Move french_fries to dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Recover french_fries:", success)
        if not success:
            return self.info
        
        # Pick and place stapler on fluted_block
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Pick stapler:", success)
        if not success:
            return self.info
        
        # Pick and place bread into dustbin
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Pick bread:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in the correct containers
        if (
            self.check_on(self.drill, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.stapler, self.fluted_block) and
            self.check_on(self.bread, self.dustbin) and
            self.check_on(self.french_fries, self.dustbin)
        ):
            return True
        return False
