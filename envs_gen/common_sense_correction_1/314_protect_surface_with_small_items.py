from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 314_protect_surface_with_small_items(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors and distractors in the environment."""
        # Create the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Create the main objects to be manipulated
        self.bottle = self.add_actor("bottle", "bottle")
        self.markpen = self.add_actor("markpen", "markpen")
        self.red_block = self.add_actor("red_block", "red_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractor objects to the environment
        distractor_list = ["pot-with-plant", "dumbbell", "scanner"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robotic actions for the task."""
        # Step 1: Place red_block on coaster
        success = self.pick_and_place(self.red_block, self.coaster)
        print("Place red_block:", success)
        if not success:
            return self.info

        # Step 2: Attempt to place markpen into bottle (wrong action)
        success = self.pick_and_place(self.markpen, self.bottle)
        print("Wrong action (markpen into bottle):", success)
        # Continue regardless of success to allow recovery

        # Step 3: Recovery - Place markpen onto coaster
        success = self.pick_and_place(self.markpen, self.coaster)
        print("Recovery (markpen onto coaster):", success)
        if not success:
            return self.info

        # Step 4: Place yellow_block on coaster
        success = self.pick_and_place(self.yellow_block, self.coaster)
        print("Place yellow_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all required items are correctly placed on the coaster."""
        # Check if all small, lightweight items are on the coaster
        if (self.check_on(self.red_block, self.coaster) and
            self.check_on(self.markpen, self.coaster) and
            self.check_on(self.yellow_block, self.coaster)):
            return True
        return False
