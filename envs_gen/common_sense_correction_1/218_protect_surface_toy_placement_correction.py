from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 218_protect_surface_toy_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the coaster as a container.
        - Add the objects: green_block, red_block, knife, toycar.
        - Add distractor objects as specified in the task description.
        """
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")

        # Add the main objects involved in the task
        self.green_block = self.add_actor("green_block", "green_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.knife = self.add_actor("knife", "knife")
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractor objects to the environment
        distractor_list = ['calculator', 'book', 'alarm-clock', 'tissue-box', 'small-speaker']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        - Place green_block on the coaster.
        - Place knife on the coaster (wrong action).
        - Recover by placing knife back on the table.
        - Place red_block and toycar on the coaster.
        """
        # Step 1: Place green_block on the coaster
        success = self.pick_and_place(self.green_block, self.coaster)
        print("Place green_block:", success)
        if not success:
            return self.info

        # Step 2: Wrong action - place knife on the coaster
        success = self.pick_and_place(self.knife, self.coaster)
        print("Wrong: Place knife on coaster:", success)
        if not success:
            return self.info

        # Step 3: Recovery - place knife back on the table
        success = self.pick_and_place(self.knife, self.table)
        print("Recover: Place knife on table:", success)
        if not success:
            return self.info

        # Step 4: Place red_block on the coaster
        success = self.pick_and_place(self.red_block, self.coaster)
        print("Place red_block:", success)
        if not success:
            return self.info

        # Step 5: Place toycar on the coaster
        success = self.pick_and_place(self.toycar, self.coaster)
        print("Place toycar:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All small, lightweight toys (green_block, red_block, toycar) must be on the coaster.
        - The knife must not be on the coaster.
        """
        if (
            self.check_on(self.green_block, self.coaster) and
            self.check_on(self.red_block, self.coaster) and
            self.check_on(self.toycar, self.coaster) and
            not self.check_on(self.knife, self.coaster)
        ):
            return True
        return False
