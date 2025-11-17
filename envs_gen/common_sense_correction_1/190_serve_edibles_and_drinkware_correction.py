from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 190_serve_edibles_and_drinkware_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Create the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Create objects that need to be placed
        self.bread = self.add_actor("bread", "bread")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.can = self.add_actor("can", "can")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractor objects to the environment
        distractor_list = ["hammer", "stapler", "toycar", "alarm-clock", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's actions in sequence"""
        # First attempt: incorrectly place tissue-box on plate
        success = self.pick_and_place(self.tissue_box, self.plate)
        print("pick place tissue-box (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: move tissue-box back to table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("pick place tissue-box (recovery):", success)
        if not success:
            return self.info
            
        # Place edible and utensil items on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("pick place bread:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("pick place cup_with_handle:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.can, self.plate)
        print("pick place can:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        return (
            self.check_on(self.bread, self.plate) and
            self.check_on(self.cup_with_handle, self.plate) and
            self.check_on(self.can, self.plate)
        )
