from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 28_organize_toys_and_drinkware_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment."""
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add objects
        self.can = self.add_actor("can", "can")
        self.toycar = self.add_actor("toycar", "toycar")
        self.red_block = self.add_actor("red_block", "red_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        
        # Add distractors
        distractor_list = ["screwdriver", "hammer", "pot-with-plant", "book", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of actions to complete the task."""
        # Step 1: Place can on coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Pick can and place on coaster:", success)
        if not success:
            return self.info

        # Step 2: Place toycar on coaster (wrong action)
        success = self.pick_and_place(self.toycar, self.coaster)
        print("Pick toycar and place on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing toycar in fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Recover toycar and place in fluted_block:", success)
        if not success:
            return self.info

        # Step 4: Place red_block in fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Pick red_block and place in fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place orange_block in fluted_block
        success = self.pick_and_place(self.orange_block, self.fluted_block)
        print("Pick orange_block and place in fluted_block:", success)
        if not success:
            return self.info

        return self.info  # All steps completed successfully

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Check if can is on coaster
        can_on_coaster = self.check_on(self.can, self.coaster)
        
        # Check if toycar is in fluted_block
        toycar_in_fluted = self.check_on(self.toycar, self.fluted_block)
        
        # Check if red_block is in fluted_block
        red_in_fluted = self.check_on(self.red_block, self.fluted_block)
        
        # Check if orange_block is in fluted_block
        orange_in_fluted = self.check_on(self.orange_block, self.fluted_block)
        
        # All conditions must be satisfied for success
        return can_on_coaster and toycar_in_fluted and red_in_fluted and orange_in_fluted
