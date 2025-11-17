from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 199_place_edible_foods_on_plate_with_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        self.plate = self.add_actor("plate", "plate")
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        
        # Add distractor objects
        distractor_list = ["calculator", "screwdriver", "shoe", "book", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # Wrong action: place non-edible item on plate
        success = self.pick_and_place(self.pot_with_plant, self.plate)
        print("Wrong action - pot-with-plant to plate:", success)
        if not success:
            return self.info
            
        # Recovery: place non-edible item back on table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Recovery action - pot-with-plant to table:", success)
        if not success:
            return self.info
            
        # Place edible foods on plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Apple to plate:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Hamburg to plate:", success)
        if not success:
            return self.info
            
        # Place non-edible block on table
        success = self.pick_and_place(self.blue_block, self.table)
        print("Blue block to table:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        return (
            self.check_on(self.apple, self.plate) and 
            self.check_on(self.hamburg, self.plate) and 
            not self.check_on(self.pot_with_plant, self.plate) and 
            not self.check_on(self.blue_block, self.plate)
        )
