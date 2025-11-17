from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 126_serve_edibles_and_drinkware_with_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Create the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Create edible items and drink containers
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        
        # Create non-food toy to be excluded
        self.blue_block = self.add_actor("blue_block", "blue_block")
        
        # Add distractor objects
        distractors = ["calculator", "screwdriver", "pot-with-plant", "alarm-clock", "tissue-box"]
        self.add_distractors(distractors)

    def play_once(self):
        """Execute the robot's actions in sequence"""
        # Initial incorrect action (blue_block on plate)
        success = self.pick_and_place(self.blue_block, self.plate)
        print("Pick blue_block and place onto plate (wrong):", success)
        if not success:
            return self.info

        # Recovery action (blue_block back to table)
        success = self.pick_and_place(self.blue_block, self.table)
        print("Pick blue_block from plate and place on table (recovery):", success)
        if not success:
            return self.info

        # Place edible items and small drink containers on plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Pick french_fries and place onto plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle, self.plate)
        print("Pick bottle and place onto plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("Pick cup_with_handle and place onto plate:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if all edible items and drink containers are on the plate
        # and the non-food item (blue_block) is not on the plate
        return (
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.bottle, self.plate) and
            self.check_on(self.cup_with_handle, self.plate) and
            not self.check_on(self.blue_block, self.plate)
        )
