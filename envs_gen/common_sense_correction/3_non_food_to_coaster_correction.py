from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 3_non_food_to_coaster_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")
        # Add objects
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.bell = self.add_actor("bell", "bell")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

    def play_once(self):
        # Step 1: Pick and place french_fries into plate (food item)
        success = self.pick_and_place(self.french_fries, self.plate)
        print("pick place french_fries:", success)
        if not success:
            return self.info

        # Step 2: Pick and place screwdriver into coaster (non-food item)
        success = self.pick_and_place(self.screwdriver, self.coaster)
        print("pick place screwdriver:", success)
        if not success:
            return self.info

        # Step 3: Pick and place bell into plate (wrong, but part of the task)
        success = self.pick_and_place(self.bell, self.plate)
        print("pick place bell:", success)
        if not success:
            return self.info

        # Step 4: Recovery: pick bell from plate and place into coaster
        if self.check_on(self.bell, self.plate):
            success = self.pick_and_place(self.bell, self.coaster)
            print("pick place bell to coaster:", success)
            if not success:
                return self.info

        # Step 5: Pick and place purple_block into coaster
        success = self.pick_and_place(self.purple_block, self.coaster)
        print("pick place purple_block:", success)
        if not success:
            return self.info

        # Step 6: Pick and place yellow_block into coaster
        success = self.pick_and_place(self.yellow_block, self.coaster)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if french_fries is on the plate (food item)
        if not self.check_on(self.french_fries, self.plate):
            return False

        # Check if non-food items are on the coaster
        if not self.check_on(self.screwdriver, self.coaster):
            return False
        if not self.check_on(self.bell, self.coaster):
            return False
        if not self.check_on(self.purple_block, self.coaster):
            return False
        if not self.check_on(self.yellow_block, self.coaster):
            return False

        return True
