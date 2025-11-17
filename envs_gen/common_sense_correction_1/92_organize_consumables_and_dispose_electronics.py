from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 92_organize_consumables_and_dispose_electronics(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: tray and dustbin
        - Objects: apple, shampoo, cup, small-speaker
        - Distractors: pet-collar, markpen, red_block, sand-clock, table-tennis
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.cup = self.add_actor("cup", "cup")
        self.small_speaker = self.add_actor("small-speaker", "small_speaker")

        # Add distractors
        distractor_list = ["pet-collar", "markpen", "red_block", "sand-clock", "table-tennis"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm:
        1. Place small-speaker on tray (wrong action)
        2. Recover by placing small-speaker into dustbin
        3. Place apple, cup, and shampoo on the tray
        """
        # Step 1: Wrong action - place small-speaker on tray
        success = self.pick_and_place(self.small_speaker, self.tray)
        print("Place small-speaker on tray (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - place small-speaker into dustbin
        success = self.pick_and_place(self.small_speaker, self.dustbin)
        print("Move small-speaker to dustbin:", success)
        if not success:
            return self.info

        # Step 3: Place edible (apple) on tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Place apple on tray:", success)
        if not success:
            return self.info

        # Step 4: Place drinkware (cup) on tray
        success = self.pick_and_place(self.cup, self.tray)
        print("Place cup on tray:", success)
        if not success:
            return self.info

        # Step 5: Place personal-care (shampoo) on tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Place shampoo on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - Apple, cup, and shampoo are on the tray
        - Small-speaker is in the dustbin
        """
        if (
            self.check_on(self.apple, self.tray) and
            self.check_on(self.cup, self.tray) and
            self.check_on(self.shampoo, self.tray) and
            self.check_on(self.small_speaker, self.dustbin)
        ):
            return True
        return False
