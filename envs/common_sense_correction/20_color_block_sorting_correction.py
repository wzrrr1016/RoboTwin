from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class color_block_sorting_correction_20(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add color blocks
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")

    def play_once(self):
        # Place primary color blocks into fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Pick and place red_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Pick and place blue_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Pick and place yellow_block:", success)
        if not success:
            return self.info

        # Place secondary color blocks into wooden_box
        success = self.pick_and_place(self.green_block, self.wooden_box)
        print("Pick and place green_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.purple_block, self.wooden_box)
        print("Pick and place purple_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.orange_block, self.wooden_box)
        print("Pick and place orange_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all primary colors are on fluted_block
        if (self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.yellow_block, self.fluted_block)):

            # Check if all secondary colors are on wooden_box
            if (self.check_on(self.green_block, self.wooden_box) and
                self.check_on(self.purple_block, self.wooden_box) and
                self.check_on(self.orange_block, self.wooden_box)):
                return True

        return False
