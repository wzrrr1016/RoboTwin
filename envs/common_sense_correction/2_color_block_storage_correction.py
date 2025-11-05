from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class color_block_storage_correction_2(Imagine_Task):
    def load_actors(self):
        # Add the required containers and objects
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.scanner = self.add_actor("scanner", "scanner")

    def play_once(self):
        # First, pick the purple_block and place it into the shoe_box
        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("pick place purple_block:", success)
        if not success:
            return self.info

        # Then, pick the scanner and place it on the table
        success = self.pick_and_place(self.scanner, self.table)
        print("pick place scanner:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the purple_block is on the shoe_box
        if not self.check_on(self.purple_block, self.shoe_box):
            return False

        # Check if the scanner is on the table
        if not self.check_on(self.scanner, self.table):
            return False

        return True
