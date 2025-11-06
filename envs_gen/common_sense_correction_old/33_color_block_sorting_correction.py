from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 33_color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add color blocks
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")

    def play_once(self):
        # Pick red_block and place into wooden_box
        success = self.pick_and_place(self.red_block, self.wooden_box)
        print("pick place red_block:", success)
        if not success:
            return self.info

        # Pick green_block and place into tray
        success = self.pick_and_place(self.green_block, self.tray)
        print("pick place green_block:", success)
        if not success:
            return self.info

        # Pick blue_block and place into tray
        success = self.pick_and_place(self.blue_block, self.tray)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        # Pick yellow_block and place into wooden_box
        success = self.pick_and_place(self.yellow_block, self.wooden_box)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

        # Pick purple_block and place into wooden_box
        success = self.pick_and_place(self.purple_block, self.wooden_box)
        print("pick place purple_block:", success)
        if not success:
            return self.info

        # Pick orange_block and place into tray
        success = self.pick_and_place(self.orange_block, self.tray)
        print("pick place orange_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check red_block is on wooden_box
        if not self.check_on(self.red_block, self.wooden_box):
            return False

        # Check green_block is on tray
        if not self.check_on(self.green_block, self.tray):
            return False

        # Check blue_block is on tray
        if not self.check_on(self.blue_block, self.tray):
            return False

        # Check yellow_block is on wooden_box
        if not self.check_on(self.yellow_block, self.wooden_box):
            return False

        # Check purple_block is on wooden_box
        if not self.check_on(self.purple_block, self.wooden_box):
            return False

        # Check orange_block is on tray
        if not self.check_on(self.orange_block, self.tray):
            return False

        return True
