from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 9_primary_color_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the tray as a container
        self.tray = self.add_actor("tray", "tray")
        
        # Add the primary color blocks
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Optional: Add non-primary color blocks (for completeness)
        self.green_block = self.add_actor("green_block", "green_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")

    def play_once(self):
        # Pick and place blue_block into tray
        success = self.pick_and_place(self.blue_block, self.tray)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        # Pick and place red_block into tray
        success = self.pick_and_place(self.red_block, self.tray)
        print("pick place red_block:", success)
        if not success:
            return self.info

        # Pick and place yellow_block into tray
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all primary color blocks are on the tray
        if (self.check_on(self.blue_block, self.tray) and
            self.check_on(self.red_block, self.tray) and
            self.check_on(self.yellow_block, self.tray)):
            return True
        return False
