from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 263_place_edibles_and_drinkware_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractors
        distractor_list = ['calculator', 'toycar', 'alarm-clock', 'shoe', 'small-speaker']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot arm should perform in the simulation.
        """
        # Step 1: Place apple on plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Place apple on plate:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place screwdriver on plate
        success = self.pick_and_place(self.screwdriver, self.plate)
        print("Place screwdriver on plate (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recovery - Place screwdriver back on table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Place screwdriver on table (recovery):", success)
        if not success:
            return self.info

        # Step 4: Place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        # Step 5: Place cup_without_handle on coaster
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Place cup_without_handle on coaster:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Check if the task was completed successfully.
        """
        # Check if apple is on the plate
        apple_on_plate = self.check_on(self.apple, self.plate)

        # Check if both cups are on the coaster
        cup1_on_coaster = self.check_on(self.cup_with_handle, self.coaster)
        cup2_on_coaster = self.check_on(self.cup_without_handle, self.coaster)

        # Check if screwdriver is not on the plate
        screwdriver_not_on_plate = not self.check_on(self.screwdriver, self.plate)

        # Return True only if all conditions are met
        return apple_on_plate and cup1_on_coaster and cup2_on_coaster and screwdriver_not_on_plate
