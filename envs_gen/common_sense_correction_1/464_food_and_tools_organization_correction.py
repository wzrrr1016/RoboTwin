from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 464_food_and_tools_organization_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the environment"""
        # Create containers
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create objects
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.can = self.add_actor("can", "can")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractors
        self.add_distractors(['pet-collar', 'pot-with-plant', 'shoe', 'book', 'tissue-box'])

    def play_once(self):
        """Execute the sequence of robot actions"""
        # Place food items on plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french_fries on plate:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.can, self.plate)
        print("Place can on plate:", success)
        if not success:
            return self.info
            
        # Incorrect placement (wrong action)
        success = self.pick_and_place(self.purple_block, self.plate)
        print("Incorrect placement of purple_block:", success)
        if not success:
            return self.info
            
        # Recovery action - move purple_block to correct container
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("Recover purple_block to fluted_block:", success)
        if not success:
            return self.info
            
        # Place tool in fluted_block
        success = self.pick_and_place(self.knife, self.fluted_block)
        print("Place knife in fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        return (self.check_on(self.french_fries, self.plate) and
                self.check_on(self.can, self.plate) and
                self.check_on(self.purple_block, self.fluted_block) and
                self.check_on(self.knife, self.fluted_block))
