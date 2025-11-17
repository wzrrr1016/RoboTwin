from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 338_place_edible_and_keep_hazardous_off_plate(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Create the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Create edible items
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.bread = self.add_actor("bread", "bread")
        
        # Create non-edible items
        self.knife = self.add_actor("knife", "knife")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractor objects
        distractor_list = ["microphone", "sand-clock", "small-speaker", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's actions in sequence"""
        # Place hamburg on plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Place hamburg:", success)
        if not success:
            return self.info

        # Place bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Place bread:", success)
        if not success:
            return self.info

        # Wrongly place knife on plate (will be corrected)
        success = self.pick_and_place(self.knife, self.plate)
        print("Place knife (wrong):", success)
        if not success:
            return self.info

        # Correct by moving knife to table
        success = self.pick_and_place(self.knife, self.table)
        print("Move knife to table:", success)
        if not success:
            return self.info

        # Place toycar on table
        success = self.pick_and_place(self.toycar, self.table)
        print("Place toycar on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if edible items are on the plate
        hamburg_on_plate = self.check_on(self.hamburg, self.plate)
        bread_on_plate = self.check_on(self.bread, self.plate)
        
        # Check if non-edible items are NOT on the plate
        knife_off_plate = not self.check_on(self.knife, self.plate)
        toycar_off_plate = not self.check_on(self.toycar, self.plate)
        
        # Return True only if all conditions are met
        return hamburg_on_plate and bread_on_plate and knife_off_plate and toycar_off_plate
