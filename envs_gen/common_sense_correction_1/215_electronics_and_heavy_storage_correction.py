from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 215_electronics_and_heavy_storage_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: tray and shoe_box
        - Objects: small-speaker, mouse, screwdriver, dumbbell
        - Distractors: baguette, pot-with-plant, book, apple, chips-tub
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.mouse = self.add_actor("mouse", "mouse")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

        # Add distractors
        distractor_list = ["baguette", "pot-with-plant", "book", "apple", "chips-tub"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        The task includes:
        1. Wrongly placing the screwdriver on the tray
        2. Recovering by placing the screwdriver into the shoe_box
        3. Placing small, portable electronic devices (mouse, small-speaker) on the tray
        4. Placing heavier metal tools or weights (dumbbell) into the shoe_box
        """
        # Step 1: Wrong placement of screwdriver on tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Pick screwdriver and place on tray (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - move screwdriver to shoe_box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Pick screwdriver from tray and place into shoe_box (recovery):", success)
        if not success:
            return self.info

        # Step 3: Place small-speaker on tray
        success = self.pick_and_place(self.small_speaker, self.tray)
        print("Pick small-speaker and place on tray:", success)
        if not success:
            return self.info

        # Step 4: Place mouse on tray
        success = self.pick_and_place(self.mouse, self.tray)
        print("Pick mouse and place on tray:", success)
        if not success:
            return self.info

        # Step 5: Place dumbbell in shoe_box
        success = self.pick_and_place(self.dumbbell, self.shoe_box)
        print("Pick dumbbell and place into shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if all objects are placed in the correct containers.
        - small-speaker and mouse should be on the tray
        - screwdriver and dumbbell should be in the shoe_box
        """
        if (self.check_on(self.small_speaker, self.tray) and
            self.check_on(self.mouse, self.tray) and
            self.check_on(self.screwdriver, self.shoe_box) and
            self.check_on(self.dumbbell, self.shoe_box)):
            return True
        return False
