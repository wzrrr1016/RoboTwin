from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 83_handle_drinkware_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: fluted_block
        - Objects: cup_with_handle, bottle, mug, stapler
        - Distractors: toycar, apple, alarm-clock, red_block, tissue-box
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the main objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.bottle = self.add_actor("bottle", "bottle")
        self.mug = self.add_actor("mug", "mug")
        self.stapler = self.add_actor("stapler", "stapler")
        
        # Add distractor objects
        distractor_list = ["toycar", "apple", "alarm-clock", "red_block", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's sequence of actions:
        1. Place bottle into fluted_block (wrong action)
        2. Recover by placing bottle on table
        3. Place cup_with_handle into fluted_block
        4. Place mug into fluted_block
        5. Place stapler on table
        """
        # Wrong action: place bottle into fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Place bottle into fluted_block (wrong):", success)
        if not success:
            return self.info

        # Recovery: place bottle onto table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover bottle to table:", success)
        if not success:
            return self.info

        # Correct action: place cup_with_handle into fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Place cup_with_handle:", success)
        if not success:
            return self.info

        # Correct action: place mug into fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug:", success)
        if not success:
            return self.info

        # Correct action: place stapler on table
        success = self.pick_and_place(self.stapler, self.table)
        print("Place stapler on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - cup_with_handle and mug are in fluted_block
        - bottle is NOT in fluted_block
        - stapler is on the table
        """
        if (self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.mug, self.fluted_block) and
            not self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.stapler, self.table)):
            return True
        return False
