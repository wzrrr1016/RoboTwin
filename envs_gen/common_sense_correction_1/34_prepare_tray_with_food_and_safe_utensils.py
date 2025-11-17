from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 34_prepare_tray_with_food_and_safe_utensils(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Adds the tray, ready-to-eat foods, and safe eating utensils.
        Adds distractor objects to the environment.
        """
        # Add the tray as the container
        self.tray = self.add_actor("tray", "tray")

        # Add the ready-to-eat foods and utensils
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")

        # Add distractor objects to the environment
        distractor_list = ["calculator", "screwdriver", "alarm-clock", "toycar", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Steps:
        1. Pick bread and place it on the tray.
        2. Pick french fries and place it on the tray.
        3. Pick knife and place it on the tray (wrong action).
        4. Pick knife from the tray and place it on the table (recovery).
        5. Pick fork and place it on the tray.
        """
        # Step 1: Pick bread and place on tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Pick bread and place on tray:", success)
        if not success:
            return self.info

        # Step 2: Pick french fries and place on tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Pick french fries and place on tray:", success)
        if not success:
            return self.info

        # Step 3: Pick knife and place on tray (wrong action)
        success = self.pick_and_place(self.knife, self.tray)
        print("Pick knife and place on tray (wrong):", success)
        if not success:
            return self.info

        # Step 4: Pick knife from tray and place on table (recovery)
        success = self.pick_and_place(self.knife, self.table)
        print("Pick knife from tray and place on table:", success)
        if not success:
            return self.info

        # Step 5: Pick fork and place on tray
        success = self.pick_and_place(self.fork, self.tray)
        print("Pick fork and place on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The tray should contain bread, french fries, and fork.
        The knife should not be on the tray.
        """
        if (
            self.check_on(self.bread, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.fork, self.tray) and
            not self.check_on(self.knife, self.tray)
        ):
            return True
        return False
