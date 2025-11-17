from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 123_liquid_holders_on_tray_correction(Imagine_Task):
    def load_actors(self):
        """
        Load the necessary actors into the simulation environment.
        - Adds the tray as a container.
        - Adds objects that may or may not hold liquids.
        - Adds distractors to the environment.
        """
        # Add the tray as a container
        self.tray = self.add_actor("tray", "tray")

        # Add objects that may or may not hold liquids
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.can = self.add_actor("can", "can")
        self.markpen = self.add_actor("markpen", "markpen")
        self.hammer = self.add_actor("hammer", "hammer")

        # Add distractors to the environment
        self.add_distractors(["calculator", "battery", "apple", "shoe", "book"])

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        - Pick and place objects based on the task logic.
        - If any action fails, return early.
        """
        # Step 1: Pick markpen and place it onto tray (wrong action)
        success = self.pick_and_place(self.markpen, self.tray)
        print("Pick markpen to tray:", success)
        if not success:
            return self.info

        # Step 2: Pick markpen from tray and place it on table (recovery)
        success = self.pick_and_place(self.markpen, self.table)
        print("Recover markpen to table:", success)
        if not success:
            return self.info

        # Step 3: Pick cup_with_handle and place it onto tray
        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Pick cup_with_handle to tray:", success)
        if not success:
            return self.info

        # Step 4: Pick can and place it onto tray
        success = self.pick_and_place(self.can, self.tray)
        print("Pick can to tray:", success)
        if not success:
            return self.info

        # Step 5: Pick hammer and place it on table
        success = self.pick_and_place(self.hammer, self.table)
        print("Pick hammer to table:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was successful.
        - The task is successful if both the cup_with_handle and can are on the tray.
        """
        return self.check_on(self.cup_with_handle, self.tray) and self.check_on(self.can, self.tray)
