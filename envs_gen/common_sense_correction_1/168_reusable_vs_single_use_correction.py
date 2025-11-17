from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 168_reusable_vs_single_use_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: tray and dustbin
        - Objects: toycar, tissue-box, book, dumbbell
        - Distractors: chips-tub, apple, baguette, french_fries, hamburg
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add required objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.book = self.add_actor("book", "book")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

        # Add distractors
        distractor_list = ["chips-tub", "apple", "baguette", "french_fries", "hamburg"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task:
        1. Place toycar on tray
        2. Place tissue-box on tray (wrong action)
        3. Move tissue-box from tray to dustbin (recovery)
        4. Place book on tray
        5. Place dumbbell on tray
        """
        # Step 1: Place toycar on tray
        success = self.pick_and_place(self.toycar, self.tray)
        print("Place toycar on tray:", success)
        if not success:
            return self.info

        # Step 2: Place tissue-box on tray (wrong action)
        success = self.pick_and_place(self.tissue_box, self.tray)
        print("Place tissue-box on tray (wrong):", success)
        if not success:
            return self.info

        # Step 3: Move tissue-box to dustbin (recovery)
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Move tissue-box to dustbin:", success)
        if not success:
            return self.info

        # Step 4: Place book on tray
        success = self.pick_and_place(self.book, self.tray)
        print("Place book on tray:", success)
        if not success:
            return self.info

        # Step 5: Place dumbbell on tray
        success = self.pick_and_place(self.dumbbell, self.tray)
        print("Place dumbbell on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - Reusable items (toycar, book, dumbbell) are on the tray
        - Single-use hygiene item (tissue-box) is in the dustbin
        """
        if (
            self.check_on(self.toycar, self.tray) and
            self.check_on(self.book, self.tray) and
            self.check_on(self.dumbbell, self.tray) and
            self.check_on(self.tissue_box, self.dustbin)
        ):
            return True
        return False
