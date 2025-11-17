from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 193_place_liquid_containers_on_coaster_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the coaster as a container.
        - Add the objects: cup_with_handle, shampoo, french_fries, and purple_block.
        - Add distractors as specified in the task description.
        """
        self.coaster = self.add_actor("coaster", "coaster")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        distractor_list = ["calculator", "screwdriver", "shoe", "book", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in one trial.
        1. Attempt to place the purple_block on the coaster (wrong action).
        2. If the purple_block is on the coaster, recover by placing it back on the table.
        3. Place the cup_with_handle and shampoo on the coaster (liquid containers).
        4. Place the french_fries on the table (food item).
        """
        # Step 1: Wrong action - place purple_block on coaster
        success = self.pick_and_place(self.purple_block, self.coaster)
        print("Wrong action (purple_block to coaster):", success)
        if not success:
            return self.info

        # Step 2: Recovery action - if purple_block is on coaster, place it back on table
        if self.check_on(self.purple_block, self.coaster):
            success = self.pick_and_place(self.purple_block, self.table)
            print("Recovery action (purple_block to table):", success)
            if not success:
                return self.info

        # Step 3: Correct action - place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        # Step 4: Correct action - place shampoo on coaster
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Place shampoo on coaster:", success)
        if not success:
            return self.info

        # Step 5: Correct action - place french_fries on table
        success = self.pick_and_place(self.french_fries, self.table)
        print("Place french_fries on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Liquid containers (cup_with_handle and shampoo) are on the coaster.
        - Solid toys (purple_block) and food (french_fries) are on the table.
        """
        if (self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.shampoo, self.coaster) and
            self.check_on(self.purple_block, self.table) and
            self.check_on(self.french_fries, self.table)):
            return True
        return False
