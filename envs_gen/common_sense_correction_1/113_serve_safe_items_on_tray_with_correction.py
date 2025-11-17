from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 113_serve_safe_items_on_tray_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the tray (container), edible items (apple, can), utensils (fork, knife),
        and distractors that are not relevant to the task.
        """
        # Add the tray as the container
        self.tray = self.add_actor("tray", "tray")

        # Add edible and utensil objects
        self.apple = self.add_actor("apple", "apple")
        self.fork = self.add_actor("fork", "fork")
        self.can = self.add_actor("can", "can")
        self.knife = self.add_actor("knife", "knife")

        # Add distractors that are not relevant to the task
        distractors = ["calculator", "screwdriver", "shoe", "toycar", "alarm-clock"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        The robot places edible and utensil items on the tray, but mistakenly places the knife
        and then recovers by moving it back to the table.
        """
        # Step 1: Pick apple and place it on the tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Pick apple and place on tray:", success)
        if not success:
            return self.info

        # Step 2: Pick fork and place it on the tray
        success = self.pick_and_place(self.fork, self.tray)
        print("Pick fork and place on tray:", success)
        if not success:
            return self.info

        # Step 3: Pick knife and place it on the tray (wrong action)
        success = self.pick_and_place(self.knife, self.tray)
        print("Pick knife and place on tray (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover by picking knife from tray and placing it on the table
        success = self.pick_and_place(self.knife, self.table)
        print("Recover knife and place on table:", success)
        if not success:
            return self.info

        # Step 5: Pick can and place it on the tray
        success = self.pick_and_place(self.can, self.tray)
        print("Pick can and place on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The task is considered successful if:
        - Apple, fork, and can are on the tray.
        - Knife is not on the tray (i.e., it was recovered and placed on the table).
        """
        if (
            self.check_on(self.apple, self.tray) and
            self.check_on(self.fork, self.tray) and
            self.check_on(self.can, self.tray) and
            not self.check_on(self.knife, self.tray)
        ):
            return True
        return False
