from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 487_food_and_nonfood_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: plate and fluted_block
        - Objects: french_fries, fork, markpen, cup_without_handle
        - Distractors: scanner, microphone, alarm-clock, sand-clock
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.fork = self.add_actor("fork", "fork")
        self.markpen = self.add_actor("markpen", "markpen")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")

        # Add distractors
        distractors = ["scanner", "microphone", "alarm-clock", "sand-clock"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task:
        1. Place edible items and eating utensils on the plate.
        2. Place small non-food objects into the fluted_block.
        """
        # Step 1: Place edible item (french_fries) on the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Pick and place french_fries on plate:", success)
        if not success:
            return self.info

        # Step 2: Place eating utensil (fork) on the plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Pick and place fork on plate:", success)
        if not success:
            return self.info

        # Step 3: Place markpen on the plate (wrong action)
        success = self.pick_and_place(self.markpen, self.plate)
        print("Pick and place markpen on plate (wrong):", success)
        if not success:
            return self.info

        # Step 4: Correct the mistake by placing markpen into fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Pick and place markpen into fluted_block (recovery):", success)
        if not success:
            return self.info

        # Step 5: Place cup_without_handle into fluted_block
        success = self.pick_and_place(self.cup_without_handle, self.fluted_block)
        print("Pick and place cup_without_handle into fluted_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully:
        - Edible items and eating utensils are on the plate.
        - Small non-food objects are in the fluted_block.
        """
        if (
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.fork, self.plate) and
            self.check_on(self.markpen, self.fluted_block) and
            self.check_on(self.cup_without_handle, self.fluted_block)
        ):
            return True
        return False
