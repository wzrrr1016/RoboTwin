from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 37_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        Containers: shoe_box, coaster
        Objects: bottle, mug, bread, apple, pink_block
        Distractors: calculator, pet-collar, table-tennis, roll-paper, battery, screwdriver
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.coaster = self.add_actor("coaster", "coaster")

        # Add objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.mug = self.add_actor("mug", "mug")
        self.bread = self.add_actor("bread", "bread")
        self.apple = self.add_actor("apple", "apple")
        self.pink_block = self.add_actor("pink_block", "pink_block")

        # Add distractors
        distractor_list = [
            "calculator", "pet-collar", "table-tennis", "roll-paper", "battery", "screwdriver"
        ]
        self.add_distractors(distractor_list)

        # Final check to ensure all actors are placed correctly
        self.check_scene()

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        The robot first makes a mistake (wrong placement), then recovers and places
        all objects correctly.
        """
        # Step 1: Wrong action - Place bottle into shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("Pick bottle into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - Place bottle into coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Recover: Pick bottle into coaster:", success)
        if not success:
            return self.info

        # Step 3: Place mug into coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Pick mug into coaster:", success)
        if not success:
            return self.info

        # Step 4: Place bread into shoe_box
        success = self.pick_and_place(self.bread, self.shoe_box)
        print("Pick bread into shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place apple into shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Pick apple into shoe_box:", success)
        if not success:
            return self.info

        # Step 6: Place pink_block into shoe_box
        success = self.pick_and_place(self.pink_block, self.shoe_box)
        print("Pick pink_block into shoe_box:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Check if all objects are placed in the correct containers:
        - Drinkware (bottle, mug) should be on the coaster
        - Non-drinkware (bread, apple, pink_block) should be in the shoe_box
        """
        if (
            self.check_on(self.bottle, self.coaster) and
            self.check_on(self.mug, self.coaster) and
            self.check_on(self.bread, self.shoe_box) and
            self.check_on(self.apple, self.shoe_box) and
            self.check_on(self.pink_block, self.shoe_box)
        ):
            return True
        return False
