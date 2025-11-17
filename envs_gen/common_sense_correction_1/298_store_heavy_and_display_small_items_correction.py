from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 298_store_heavy_and_display_small_items_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: shoe_box, fluted_block
        - Objects: drill, stapler, toycar, mug
        - Distractors: baguette, apple, hamburg, chips-tub
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.drill = self.add_actor("drill", "drill")
        self.stapler = self.add_actor("stapler", "stapler")
        self.toycar = self.add_actor("toycar", "toycar")
        self.mug = self.add_actor("mug", "mug")

        # Add distractors
        distractor_list = ["baguette", "apple", "hamburg", "chips-tub"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task:
        1. Pick drill and place it into shoe_box
        2. Pick mug and place it into shoe_box (wrong)
        3. Pick mug from shoe_box and place it onto fluted_block (recovery)
        4. Pick stapler and place it onto fluted_block
        5. Pick toycar and place it onto fluted_block
        """
        # Step 1: Place drill in shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Pick drill and place into shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Place mug in shoe_box (wrong action)
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Pick mug and place into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing mug on fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Pick mug and place onto fluted_block (recovery):", success)
        if not success:
            return self.info

        # Step 4: Place stapler on fluted_block
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Pick stapler and place onto fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place toycar on fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Pick toycar and place onto fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task is successfully completed by verifying the final positions of the objects:
        - Drill is in shoe_box
        - Stapler, toycar, and mug are on fluted_block
        """
        if (
            self.check_on(self.drill, self.shoe_box) and
            self.check_on(self.stapler, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.mug, self.fluted_block)
        ):
            return True
        return False
