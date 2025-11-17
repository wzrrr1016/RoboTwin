from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 118_toy_and_metal_sort_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        - Containers: coaster, shoe_box
        - Objects: toycar, screwdriver, bell, yellow_block
        - Distractors: baguette, book, apple, tissue-box
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.bell = self.add_actor("bell", "bell")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Add distractors
        distractor_list = ["baguette", "book", "apple", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Actions:
        1. Place toycar on coaster
        2. Place screwdriver on coaster (wrong)
        3. Move screwdriver to shoe_box (recovery)
        4. Place bell in shoe_box
        5. Place yellow_block on coaster
        """
        # Step 1: Place toycar on coaster
        success = self.pick_and_place(self.toycar, self.coaster)
        print("Place toycar on coaster:", success)
        if not success:
            return self.info

        # Step 2: Place screwdriver on coaster (wrong)
        success = self.pick_and_place(self.screwdriver, self.coaster)
        print("Place screwdriver on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 3: Move screwdriver to shoe_box (recovery)
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Move screwdriver to shoe_box:", success)
        if not success:
            return self.info

        # Step 4: Place bell in shoe_box
        success = self.pick_and_place(self.bell, self.shoe_box)
        print("Place bell in shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place yellow_block on coaster
        success = self.pick_and_place(self.yellow_block, self.coaster)
        print("Place yellow_block on coaster:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task is successfully completed by verifying:
        - toycar and yellow_block are on the coaster
        - screwdriver and bell are in the shoe_box
        """
        return (
            self.check_on(self.toycar, self.coaster) and
            self.check_on(self.yellow_block, self.coaster) and
            self.check_on(self.screwdriver, self.shoe_box) and
            self.check_on(self.bell, self.shoe_box)
        )
