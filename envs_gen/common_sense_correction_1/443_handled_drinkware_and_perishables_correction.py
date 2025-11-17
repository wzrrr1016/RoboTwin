from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 443_handled_drinkware_and_perishables_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the fluted_block container, handled drinkware (mug and cup_with_handle),
        perishable foods (apple and bread), and distractor objects.
        """
        # Add the fluted_block container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add handled drinkware
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")

        # Add perishable foods
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")

        # Add distractor objects
        distractor_list = ["screwdriver", "toycar", "book", "small-speaker", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        The robot will:
        1. Place the mug into the fluted_block.
        2. Place the cup_with_handle into the fluted_block.
        3. Attempt to place the apple into the fluted_block (this is a wrong action).
        4. If step 3 fails, recover by placing the apple on the table.
        5. Place the bread on the table.
        """
        # Step 1: Place mug into fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug:", success)
        if not success:
            return self.info

        # Step 2: Place cup_with_handle into fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Place cup_with_handle:", success)
        if not success:
            return self.info

        # Step 3: Attempt to place apple into fluted_block (wrong action)
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple (wrong):", success)
        if not success:
            # Step 4: Recovery - place apple on the table
            success = self.pick_and_place(self.apple, self.table)
            print("Recovery apple:", success)
            if not success:
                return self.info

        # Step 5: Place bread on the table
        success = self.pick_and_place(self.bread, self.table)
        print("Place bread:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was successfully completed.
        The task is considered successful if:
        - The mug and cup_with_handle are in the fluted_block.
        - The apple and bread are on the table.
        """
        if (
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.apple, self.table) and
            self.check_on(self.bread, self.table)
        ):
            return True
        return False
