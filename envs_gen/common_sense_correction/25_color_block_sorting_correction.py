from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 25_color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.plate = self.add_actor("plate", "plate")
        # Add objects
        self.green_block = self.add_actor("green_block", "green_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.apple = self.add_actor("apple", "apple")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.stapler = self.add_actor("stapler", "stapler")

    def play_once(self):
        # Pick red_block (primary color) and place into wooden_box
        success = self.pick_and_place(self.red_block, self.wooden_box)
        print("pick place red_block:", success)
        if not success:
            return self.info

        # Pick green_block (secondary color) and place into plate
        success = self.pick_and_place(self.green_block, self.plate)
        print("pick place green_block:", success)
        if not success:
            return self.info

        # Pick purple_block (secondary color) and place into plate
        success = self.pick_and_place(self.purple_block, self.plate)
        print("pick place purple_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if red_block is on wooden_box
        if not self.check_on(self.red_block, self.wooden_box):
            return False
        # Check if green_block is on plate
        if not self.check_on(self.green_block, self.plate):
            return False
        # Check if purple_block is on plate
        if not self.check_on(self.purple_block, self.plate):
            return False
        return True
