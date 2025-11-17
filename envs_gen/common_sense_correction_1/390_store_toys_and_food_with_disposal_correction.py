from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 390_store_toys_and_food_with_disposal_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: shoe_box and dustbin
        - Objects: red_block, yellow_block, shampoo, apple
        - Distractors: calculator, screwdriver, alarm-clock, book, small-speaker
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.apple = self.add_actor("apple", "apple")

        # Add distractors
        distractor_list = ["calculator", "screwdriver", "alarm-clock", "book", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Actions:
        1. Pick red_block and place it into shoe_box
        2. Pick yellow_block and place it into shoe_box
        3. Pick apple and place it into dustbin (wrong)
        4. Pick apple from dustbin and place it into shoe_box (recovery)
        5. Pick shampoo and place it into dustbin
        """
        # Step 1: Place red_block into shoe_box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Place red_block into shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Place yellow_block into shoe_box
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("Place yellow_block into shoe_box:", success)
        if not success:
            return self.info

        # Step 3: Place apple into dustbin (wrong action)
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Place apple into dustbin (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover apple and place it into shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Recover apple and place into shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place shampoo into dustbin
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Place shampoo into dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed by verifying the final positions of all objects.
        - red_block and yellow_block (solid small toys) should be in shoe_box
        - apple (edible item) should be in shoe_box
        - shampoo (empty/disposable personal-care bottle) should be in dustbin
        """
        if (
            self.check_on(self.red_block, self.shoe_box) and
            self.check_on(self.yellow_block, self.shoe_box) and
            self.check_on(self.apple, self.shoe_box) and
            self.check_on(self.shampoo, self.dustbin)
        ):
            return True
        return False
