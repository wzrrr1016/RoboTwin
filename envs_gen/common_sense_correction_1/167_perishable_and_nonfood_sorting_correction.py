from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 167_perishable_and_nonfood_sorting_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        Containers: tray, shoe_box
        Objects: apple, bread, shampoo, yellow_block
        Distractors: calculator, screwdriver, hammer, book, battery
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add main objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Add distractors
        distractor_list = ["calculator", "screwdriver", "hammer", "book", "battery"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Actions:
        1. Pick shampoo and place it onto tray (wrong)
        2. Pick shampoo from tray and place it into shoe_box (recovery)
        3. Pick apple and place it onto tray
        4. Pick bread and place it onto tray
        5. Pick yellow_block and place it into shoe_box
        """
        # Step 1: Wrong action - place shampoo on tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Wrong placement of shampoo:", success)
        if not success:
            return self.info

        # Step 2: Recovery - place shampoo into shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Recovery placement of shampoo:", success)
        if not success:
            return self.info

        # Step 3: Place apple on tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Place apple:", success)
        if not success:
            return self.info

        # Step 4: Place bread on tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Place bread:", success)
        if not success:
            return self.info

        # Step 5: Place yellow_block into shoe_box
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("Place yellow block:", success)
        if not success:
            return self.info

        return self.info  # Task completed successfully

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of all objects.
        """
        if (
            self.check_on(self.apple, self.tray) and
            self.check_on(self.bread, self.tray) and
            self.check_on(self.shampoo, self.shoe_box) and
            self.check_on(self.yellow_block, self.shoe_box)
        ):
            return True
        return False
