from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 272_liquid_and_personal_care_organizing_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the container (fluted_block).
        - Add the relevant objects (mug, shampoo, bread, red_block).
        - Add distractor objects as specified in the task.
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the relevant objects
        self.mug = self.add_actor("mug", "mug")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.bread = self.add_actor("bread", "bread")
        self.red_block = self.add_actor("red_block", "red_block")

        # Add distractor objects
        distractor_list = ["calculator", "hammer", "shoe", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - Pick and place correct items into the organizer.
        - Handle incorrect placement and recovery.
        - Place the red_block on the table (as per the action list).
        """
        # Step 1: Pick and place mug into fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Pick place mug:", success)
        if not success:
            return self.info

        # Step 2: Pick and place shampoo into fluted_block
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Pick place shampoo:", success)
        if not success:
            return self.info

        # Step 3: Incorrectly place bread into fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Pick place bread (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recovery: Place bread back on the table
        success = self.pick_and_place(self.bread, self.table)
        print("Recover bread to table:", success)
        if not success:
            return self.info

        # Step 5: Place red_block on the table (as per the action list)
        success = self.pick_and_place(self.red_block, self.table)
        print("Pick place red_block on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Mug and shampoo should be in the fluted_block.
        - Bread and red_block should be on the table.
        """
        if (
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.shampoo, self.fluted_block) and
            self.check_on(self.bread, self.table) and
            self.check_on(self.red_block, self.table)
        ):
            return True
        return False
