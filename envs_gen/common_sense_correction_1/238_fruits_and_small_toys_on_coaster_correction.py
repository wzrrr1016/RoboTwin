from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 238_fruits_and_small_toys_on_coaster_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        - Add the coaster as a container.
        - Add the required objects: apple, toycar, green_block, and dumbbell.
        - Add distractors as specified in the task description.
        """
        self.coaster = self.add_actor("coaster", "coaster")
        self.apple = self.add_actor("apple", "apple")
        self.toycar = self.add_actor("toycar", "toycar")
        self.green_block = self.add_actor("green_block", "green_block")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        
        # Add distractors to the environment
        distractor_list = ["calculator", "hammer", "pot-with-plant", "alarm-clock", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Pick apple and place it on the coaster.
        2. Pick toycar and place it on the coaster.
        3. Pick dumbbell and place it on the coaster (wrong action).
        4. Pick dumbbell from the coaster and place it on the table (recovery).
        5. Pick green_block and place it on the coaster.
        """
        # Step 1: Place apple on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Pick and place apple:", success)
        if not success:
            return self.info

        # Step 2: Place toycar on coaster
        success = self.pick_and_place(self.toycar, self.coaster)
        print("Pick and place toycar:", success)
        if not success:
            return self.info

        # Step 3: Wrongly place dumbbell on coaster
        success = self.pick_and_place(self.dumbbell, self.coaster)
        print("Pick and place dumbbell (wrong):", success)
        if not success:
            return self.info

        # Step 4: Correct the error by placing dumbbell on the table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Recover dumbbell to table:", success)
        if not success:
            return self.info

        # Step 5: Place green_block on coaster
        success = self.pick_and_place(self.green_block, self.coaster)
        print("Pick and place green_block:", success)
        if not success:
            return self.info

        return self.info  # Return info if all steps succeed

    def check_success(self):
        """
        Check if the task is successfully completed:
        - Apple, toycar, and green_block are on the coaster.
        - Dumbbell is on the table (not on the coaster).
        """
        apple_on_coaster = self.check_on(self.apple, self.coaster)
        toycar_on_coaster = self.check_on(self.toycar, self.coaster)
        green_block_on_coaster = self.check_on(self.green_block, self.coaster)
        dumbbell_on_table = self.check_on(self.dumbbell, self.table)
        
        return all([
            apple_on_coaster,
            toycar_on_coaster,
            green_block_on_coaster,
            dumbbell_on_table
        ])
