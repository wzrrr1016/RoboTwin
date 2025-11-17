from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 90_serve_food_store_sharp_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Adds the specified objects and distractors.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add task-relevant objects
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.knife = self.add_actor("knife", "knife")

        # Add distractors as specified in the task
        distractor_list = ['calculator', 'alarm-clock', 'shoe', 'toycar', 'pot-with-plant']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        Includes a wrong action followed by a recovery action.
        """
        # 1. Wrong action: Place tissue-box on tray
        success = self.pick_and_place(self.tissue_box, self.tray)
        print("Place tissue-box on tray (wrong):", success)
        if not success:
            return self.info

        # 2. Recovery action: Move tissue-box from tray to wooden_box
        success = self.pick_and_place(self.tissue_box, self.wooden_box)
        print("Recover: tissue-box to wooden_box:", success)
        if not success:
            return self.info

        # 3. Place ready-to-eat foods on tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french fries on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bread, self.tray)
        print("Place bread on tray:", success)
        if not success:
            return self.info

        # 4. Place sharp or single-use hygiene items into wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Place knife in wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        Verifies that all required objects are in the correct containers.
        """
        if (
            self.check_on(self.bread, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.tissue_box, self.wooden_box) and
            self.check_on(self.knife, self.wooden_box)
        ):
            return True
        return False
