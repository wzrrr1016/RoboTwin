from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 155_organize_edible_and_drinkable_items(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Create the fluted_block container.
        - Add edible/drinkable objects: mug, bottle, french_fries.
        - Add a toy object: purple_block.
        - Add distractors as specified in the task.
        """
        # Create the fluted_block container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add edible/drinkable objects
        self.mug = self.add_actor("mug", "mug")
        self.bottle = self.add_actor("bottle", "bottle")
        self.french_fries = self.add_actor("french_fries", "french_fries")

        # Add a toy object (purple_block)
        self.purple_block = self.add_actor("purple_block", "purple_block")

        # Add distractors to the environment
        distractor_list = ['screwdriver', 'stapler', 'alarm-clock', 'shoe', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of robot actions:
        1. Place purple_block into fluted_block (wrong action).
        2. Recover by placing purple_block back on the table.
        3. Place edible/drinkable items into fluted_block.
        """
        # Step 1: Place purple_block into fluted_block (wrong action)
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("Place purple_block into fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recover by placing purple_block back on the table
        success = self.pick_and_place(self.purple_block, self.table)
        print("Recover purple_block to table:", success)
        if not success:
            return self.info

        # Step 3: Place edible/drinkable items into fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Place bottle:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Place french_fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successful:
        - All edible/drinkable items are on the fluted_block.
        - The toy (purple_block) is not on the fluted_block.
        """
        if (
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.french_fries, self.fluted_block) and
            not self.check_on(self.purple_block, self.fluted_block)
        ):
            return True
        return False
