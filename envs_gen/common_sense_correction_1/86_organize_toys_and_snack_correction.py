from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 86_organize_toys_and_snack_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

        # Add distractors
        distractor_list = ["calculator", "screwdriver", "hammer", "stapler", "markpen"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        """
        # Place blue block on tray
        success = self.pick_and_place(self.blue_block, self.tray)
        print("Place blue block:", success)
        if not success:
            return self.info

        # Place red block on tray
        success = self.pick_and_place(self.red_block, self.tray)
        print("Place red block:", success)
        if not success:
            return self.info

        # Place french fries on tray (wrong action)
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french fries (wrong):", success)
        if not success:
            return self.info

        # Move french fries to wooden box (recovery action)
        success = self.pick_and_place(self.french_fries, self.wooden_box)
        print("Move french fries to wooden box:", success)
        if not success:
            return self.info

        # Place green block on tray
        success = self.pick_and_place(self.green_block, self.tray)
        print("Place green block:", success)
        if not success:
            return self.info

        # Place pot with plant on tray
        success = self.pick_and_place(self.pot_with_plant, self.tray)
        print("Place pot with plant:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of the objects.
        """
        # Check if all toys and the plant are on the tray
        # and if the edible snack is in the wooden box
        if (self.check_on(self.blue_block, self.tray) and
            self.check_on(self.red_block, self.tray) and
            self.check_on(self.green_block, self.tray) and
            self.check_on(self.pot_with_plant, self.tray) and
            self.check_on(self.french_fries, self.wooden_box)):
            return True
        return False
