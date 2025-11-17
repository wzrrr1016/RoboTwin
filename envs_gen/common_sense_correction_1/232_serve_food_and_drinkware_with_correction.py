from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 232_serve_food_and_drinkware_with_correction(Imagine_Task):
    def load_actors(self):
        # Load required objects and containers
        self.plate = self.add_actor("plate", "plate")
        self.apple = self.add_actor("apple", "apple")
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.red_block = self.add_actor("red_block", "red_block")
        
        # Add distractors to the environment
        distractor_list = ["calculator", "screwdriver", "toycar", "alarm-clock", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place apple on the plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Pick and place apple:", success)
        if not success:
            return self.info

        # Step 2: Place red_block on the plate (wrong action)
        success = self.pick_and_place(self.red_block, self.plate)
        print("Pick and place red_block (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing red_block back on the table
        success = self.pick_and_place(self.red_block, self.table)
        print("Pick and place red_block back to table:", success)
        if not success:
            return self.info

        # Step 4: Place mug on the plate
        success = self.pick_and_place(self.mug, self.plate)
        print("Pick and place mug:", success)
        if not success:
            return self.info

        # Step 5: Place cup_with_handle on the plate
        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("Pick and place cup_with_handle:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if edible items and drinkware are on the plate
        apple_on_plate = self.check_on(self.apple, self.plate)
        mug_on_plate = self.check_on(self.mug, self.plate)
        cup_on_plate = self.check_on(self.cup_with_handle, self.plate)
        
        # Ensure red_block is not on the plate (recovery successful)
        red_block_not_on_plate = not self.check_on(self.red_block, self.plate)
        
        return apple_on_plate and mug_on_plate and cup_on_plate and red_block_not_on_plate
