from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 182_place_edibles_into_fluted_block_with_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment."""
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add edible items
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add small solid toy blocks
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.green_block = self.add_actor("green_block", "green_block")
        
        # Add distractors
        distractor_list = ["calculator", "screwdriver", "pot-with-plant", "shoe", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Define the sequence of robot actions for the task."""
        # Wrong action: pick yellow_block and place into fluted_block
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Pick yellow_block into fluted_block:", success)
        if not success:
            return self.info

        # Recovery: pick yellow_block from fluted_block and place onto table
        success = self.pick_and_place(self.yellow_block, self.table)
        print("Recover yellow_block to table:", success)
        if not success:
            return self.info

        # Pick apple and place into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Pick apple into fluted_block:", success)
        if not success:
            return self.info

        # Pick french_fries and place into fluted_block
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Pick french_fries into fluted_block:", success)
        if not success:
            return self.info

        # Pick green_block and place onto table
        success = self.pick_and_place(self.green_block, self.table)
        print("Pick green_block onto table:", success)
        if not success:
            return self.info

        return self.info  # All actions completed successfully

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Check if edible items are in the fluted_block
        apple_on_fluted = self.check_on(self.apple, self.fluted_block)
        french_fries_on_fluted = self.check_on(self.french_fries, self.fluted_block)
        
        # Check if toy blocks are on the table
        yellow_on_table = self.check_on(self.yellow_block, self.table)
        green_on_table = self.check_on(self.green_block, self.table)
        
        # Return True if all conditions are met
        return all([apple_on_fluted, french_fries_on_fluted, yellow_on_table, green_on_table])
