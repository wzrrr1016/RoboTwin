from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 6_edible_non_edible_separation_correction(Imagine_Task):
    def load_actors(self):
        # Add required containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add task objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.can = self.add_actor("can", "can")
        self.mug = self.add_actor("mug", "mug")
        
        # Add distractors
        distractors = ['calculator', 'pet-collar', 'table-tennis', 'battery', 'fluted_block', 'alarm-clock']
        self.add_distractors(distractors)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Place edible items on plate
        success = self.pick_and_place(self.apple, self.plate)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.bread, self.plate)
        if not success:
            return self.info
            
        # Wrong placement of can (needs recovery)
        success = self.pick_and_place(self.can, self.plate)
        if not success:
            return self.info
            
        # Recovery - move can to dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        if not success:
            return self.info
            
        # Place non-edible mug in dustbin
        success = self.pick_and_place(self.mug, self.dustbin)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Verify final positions
        return (
            self.check_on(self.apple, self.plate) and
            self.check_on(self.bread, self.plate) and
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.mug, self.dustbin)
        )
