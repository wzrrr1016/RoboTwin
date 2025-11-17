from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 102_serve_and_store_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the environment.
        - Containers: tray and shoe_box
        - Objects: french_fries, cup, screwdriver, bell
        - Distractors: pot-with-plant, shoe, book, tissue-box, red_block
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects for the task
        self.french_fries = self.add_actor("french_fries", "french_fries_0")
        self.cup = self.add_actor("cup", "cup_0")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver_0")
        self.bell = self.add_actor("bell", "bell_0")

        # Add distractors to the environment
        distractor_list = ["pot-with-plant", "shoe", "book", "tissue-box", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        - Place eating/drinking items on the tray
        - Place tools or noisy items in the shoe_box
        - Include a recovery step for the screwdriver
        """
        # Step 1: Place french fries on the tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french fries on tray:", success)
        if not success:
            return self.info

        # Step 2: Place cup on the tray
        success = self.pick_and_place(self.cup, self.tray)
        print("Place cup on tray:", success)
        if not success:
            return self.info

        # Step 3: Wrongly place screwdriver on the tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Wrongly place screwdriver on tray:", success)
        if not success:
            return self.info

        # Step 4: Recovery: Move screwdriver to the shoe_box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Move screwdriver to shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place bell in the shoe_box
        success = self.pick_and_place(self.bell, self.shoe_box)
        print("Place bell in shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Eating/drinking items (french_fries, cup) are on the tray
        - Tools/noisy items (screwdriver, bell) are in the shoe_box
        """
        if (
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.cup, self.tray) and
            self.check_on(self.screwdriver, self.shoe_box) and
            self.check_on(self.bell, self.shoe_box)
        ):
            return True
        return False
