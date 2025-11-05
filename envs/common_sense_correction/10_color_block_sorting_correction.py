from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class color_block_sorting_correction_10(Imagine_Task):
    def load_actors(self):
        # Add the containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add the color blocks
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")

    def play_once(self):
        # Step 1: Pick red_block and place into plate (wrong)
        success = self.pick_and_place(self.red_block, self.plate)
        print("pick place red_block into plate:", success)
        if not success:
            return self.info

        # Step 2: Pick red_block from plate and place into coaster
        success = self.pick_and_place(self.red_block, self.coaster)
        print("pick place red_block into coaster:", success)
        if not success:
            return self.info

        # Step 3: Pick blue_block and place into coaster
        success = self.pick_and_place(self.blue_block, self.coaster)
        print("pick place blue_block into coaster:", success)
        if not success:
            return self.info

        # Step 4: Pick green_block and place into plate
        success = self.pick_and_place(self.green_block, self.plate)
        print("pick place green_block into plate:", success)
        if not success:
            return self.info

        # Step 5: Pick orange_block and place into plate
        success = self.pick_and_place(self.orange_block, self.plate)
        print("pick place orange_block into plate:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if red_block and blue_block are on coaster
        red_on_coaster = self.check_on(self.red_block, self.coaster)
        blue_on_coaster = self.check_on(self.blue_block, self.coaster)
        
        # Check if green_block and orange_block are on plate
        green_on_plate = self.check_on(self.green_block, self.plate)
        orange_on_plate = self.check_on(self.orange_block, self.plate)

        return red_on_coaster and blue_on_coaster and green_on_plate and orange_on_plate
