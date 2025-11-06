from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 43_recyclable_food_separation_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Add objects
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.can = self.add_actor("can", "can")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")

    def play_once(self):
        # Step 1: Pick and place french fries into tray (correct)
        success = self.pick_and_place(self.french_fries, self.tray)
        print("pick place french fries:", success)
        if not success:
            return self.info

        # Step 2: Pick and place can into tray (wrong)
        success = self.pick_and_place(self.can, self.tray)
        print("pick place can (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick can from tray and place into dustbin (recovery)
        success = self.pick_and_place(self.can, self.dustbin)
        print("pick place can (correct):", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if french fries are on the tray
        if not self.check_on(self.french_fries, self.tray):
            return False
        # Check if can is on the dustbin
        if not self.check_on(self.can, self.dustbin):
            return False
        return True
