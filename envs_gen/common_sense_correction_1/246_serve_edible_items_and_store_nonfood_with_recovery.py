from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 246_serve_edible_items_and_store_nonfood_with_recovery(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: plate and shoe_box
        - Objects: hamburg, mug, french_fries, mouse
        - Distractors: pot-with-plant, toycar, dumbbell, red_block, purple_block
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.mug = self.add_actor("mug", "mug")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.mouse = self.add_actor("mouse", "mouse")

        # Add distractors
        distractors = ["pot-with-plant", "toycar", "dumbbell", "red_block", "purple_block"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Place hamburg on the plate
        - Place mug on the plate (wrong action)
        - Move mug from the plate to the shoe_box (recovery)
        - Place french_fries on the plate
        - Place mouse in the shoe_box
        """
        # Place hamburg on the plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Place hamburg on plate:", success)
        if not success:
            return self.info

        # Place mug on the plate (wrong action)
        success = self.pick_and_place(self.mug, self.plate)
        print("Place mug on plate (wrong):", success)
        if not success:
            return self.info

        # Move mug from the plate to the shoe_box (recovery)
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Recover: Place mug into shoe_box:", success)
        if not success:
            return self.info

        # Place french_fries on the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french_fries on plate:", success)
        if not success:
            return self.info

        # Place mouse in the shoe_box
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Place mouse into shoe_box:", success)
        if not success:
            return self.info

        return self.info  # Task completed successfully

    def check_success(self):
        """
        Check if the task was completed successfully.
        - hamburg and french_fries are on the plate
        - mug and mouse are in the shoe_box
        """
        if (
            self.check_on(self.hamburg, self.plate) and
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.mug, self.shoe_box) and
            self.check_on(self.mouse, self.shoe_box)
        ):
            return True
        return False
