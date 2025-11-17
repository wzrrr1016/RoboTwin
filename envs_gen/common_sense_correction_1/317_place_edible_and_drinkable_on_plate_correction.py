from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 317_place_edible_and_drinkable_on_plate_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        Includes containers, edible/drinkable objects, and non-edible objects.
        """
        # Add the plate as a container
        self.plate = self.add_actor("plate", "plate")
        
        # Add edible/drinkable objects
        self.apple = self.add_actor("apple", "apple")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add non-edible objects that need to be placed on the table
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractor objects to the environment
        distractor_list = ["screwdriver", "hammer", "dumbbell", "book", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm.
        Includes both correct and recovery actions.
        """
        # Wrong action: Place small-speaker on plate (incorrect)
        success = self.pick_and_place(self.small_speaker, self.plate)
        print("pick place small_speaker on plate:", success)
        if not success:
            return self.info

        # Recovery action: Remove small-speaker from plate to table
        success = self.pick_and_place(self.small_speaker, self.table)
        print("pick place small_speaker on table:", success)
        if not success:
            return self.info

        # Correct actions: Place edible/drinkable items on the plate
        success = self.pick_and_place(self.apple, self.plate)
        print("pick place apple:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle, self.plate)
        print("pick place bottle:", success)
        if not success:
            return self.info

        # Place non-edible item on the table
        success = self.pick_and_place(self.yellow_block, self.table)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        Success criteria:
        - Apple and bottle are on the plate
        - Small-speaker is not on the plate
        """
        # Check if edible/drinkable items are on the plate
        apple_on_plate = self.check_on(self.apple, self.plate)
        bottle_on_plate = self.check_on(self.bottle, self.plate)
        
        # Check if non-edible item is not on the plate
        small_speaker_not_on_plate = not self.check_on(self.small_speaker, self.plate)
        
        # Return True if all conditions are met
        return apple_on_plate and bottle_on_plate and small_speaker_not_on_plate
