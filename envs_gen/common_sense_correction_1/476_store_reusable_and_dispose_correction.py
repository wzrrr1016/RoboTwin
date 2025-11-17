from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 476_store_reusable_and_dispose_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        Adds containers, target objects, and distractors.
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add target objects
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.bottle = self.add_actor("bottle", "bottle")
        self.mug = self.add_actor("mug", "mug")
        self.markpen = self.add_actor("markpen", "markpen")
        
        # Add distractors
        distractor_list = ['apple', 'baguette', 'french_fries', 'hamburg']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task.
        Includes error handling to stop execution if any step fails.
        """
        # Place blue block in wooden box
        success = self.pick_and_place(self.blue_block, self.wooden_box)
        print("Place blue_block:", success)
        if not success:
            return self.info

        # Place bottle in dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Place bottle:", success)
        if not success:
            return self.info

        # Initial wrong placement of mug in dustbin
        success = self.pick_and_place(self.mug, self.dustbin)
        print("Place mug (wrong):", success)
        if not success:
            return self.info

        # Recovery: move mug to wooden box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Recover mug:", success)
        if not success:
            return self.info

        # Place markpen in wooden box
        success = self.pick_and_place(self.markpen, self.wooden_box)
        print("Place markpen:", success)
        if not success:
            return self.info

        # Place orange block in wooden box
        success = self.pick_and_place(self.orange_block, self.wooden_box)
        print("Place orange_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify that all objects are in their correct final positions.
        Returns True if all placements are correct, False otherwise.
        """
        return (
            self.check_on(self.blue_block, self.wooden_box) and
            self.check_on(self.bottle, self.dustbin) and
            self.check_on(self.mug, self.wooden_box) and
            self.check_on(self.markpen, self.wooden_box) and
            self.check_on(self.orange_block, self.wooden_box)
        )
