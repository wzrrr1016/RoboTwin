from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 499_drinkware_and_toys_placement_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment."""
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.tray = self.add_actor("tray", "tray")
        
        # Add drinkware and blocks
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractors from the task description
        distractor_list = ['shoe', 'book', 'tissue-box', 'pot-with-plant', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of pick-and-place actions."""
        # 1. Pick mug and place on coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Pick and place mug on coaster:", success)
        if not success:
            return self.info

        # 2. Pick blue_block and place on coaster (wrong)
        success = self.pick_and_place(self.blue_block, self.coaster)
        print("Pick and place blue_block on coaster (wrong):", success)
        if not success:
            return self.info

        # 3. Pick blue_block from coaster and place on tray (recovery)
        success = self.pick_and_place(self.blue_block, self.tray)
        print("Pick and place blue_block on tray (recovery):", success)
        if not success:
            return self.info

        # 4. Pick cup_without_handle and place on coaster
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Pick and place cup_without_handle on coaster:", success)
        if not success:
            return self.info

        # 5. Pick yellow_block and place on tray
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("Pick and place yellow_block on tray:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """Verify if all objects are placed correctly."""
        # Check if drinkware is on the coaster
        drinkware_on_coaster = (
            self.check_on(self.mug, self.coaster) and 
            self.check_on(self.cup_without_handle, self.coaster)
        )
        
        # Check if solid blocks are on the tray
        blocks_on_tray = (
            self.check_on(self.blue_block, self.tray) and 
            self.check_on(self.yellow_block, self.tray)
        )
        
        return drinkware_on_coaster and blocks_on_tray
