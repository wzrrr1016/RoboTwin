from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 171_food_vs_toys_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.red_block = self.add_actor("red_block", "red_block")
        self.hammer = self.add_actor("hammer", "hammer")

        # Add distractors
        distractor_list = ["calculator", "pot-with-plant", "shoe", "tissue-box", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        """
        # Step 1: Place apple on the plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Pick and place apple:", success)
        if not success:
            return self.info

        # Step 2: Place french fries on the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Pick and place french fries:", success)
        if not success:
            return self.info

        # Step 3: Place red_block on the plate (wrong action)
        success = self.pick_and_place(self.red_block, self.plate)
        print("Pick and place red_block on plate (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recovery: Move red_block from plate to tray
        success = self.pick_and_place(self.red_block, self.tray)
        print("Pick and place red_block on tray (recovery):", success)
        if not success:
            return self.info

        # Step 5: Place hammer on the tray
        success = self.pick_and_place(self.hammer, self.tray)
        print("Pick and place hammer on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of the objects.
        """
        # Check if all required objects are in their correct containers
        if (self.check_on(self.apple, self.plate) and
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.red_block, self.tray) and
            self.check_on(self.hammer, self.tray)):
            return True
        return False
