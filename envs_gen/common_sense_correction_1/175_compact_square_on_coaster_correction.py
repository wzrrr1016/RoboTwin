from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 175_compact_square_on_coaster_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add target objects
        self.green_block = self.add_actor("green_block", "green_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.hammer = self.add_actor("hammer", "hammer")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractors
        distractor_list = ["apple", "baguette", "shoe", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # 1. Place green_block on coaster
        success = self.pick_and_place(self.green_block, self.coaster)
        print("Place green_block:", success)
        if not success:
            return self.info

        # 2. Place hammer on coaster (wrong action)
        success = self.pick_and_place(self.hammer, self.coaster)
        print("Place hammer (wrong):", success)
        if not success:
            return self.info

        # 3. Move hammer back to table (recovery)
        success = self.pick_and_place(self.hammer, self.table)
        print("Move hammer to table:", success)
        if not success:
            return self.info

        # 4. Place purple_block on coaster
        success = self.pick_and_place(self.purple_block, self.coaster)
        print("Place purple_block:", success)
        if not success:
            return self.info

        # 5. Place toycar on table
        success = self.pick_and_place(self.toycar, self.table)
        print("Place toycar on table:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Task success condition: both blocks on coaster
        if (self.check_on(self.green_block, self.coaster) and 
            self.check_on(self.purple_block, self.coaster)):
            return True
        return False
