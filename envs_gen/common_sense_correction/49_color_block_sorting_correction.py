from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 49_color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.tray = self.add_actor("tray", "tray")

        # Add primary and secondary color blocks
        self.red_block = self.add_actor("red_block", "red_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")

    def play_once(self):
        # Pick and place primary color blocks into shoe_box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("pick place red_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.shoe_box)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

        # Pick and place secondary color blocks into tray
        success = self.pick_and_place(self.orange_block, self.tray)
        print("pick place orange_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.green_block, self.tray)
        print("pick place green_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.purple_block, self.tray)
        print("pick place purple_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all primary color blocks are in shoe_box
        primary_in_shoe = (
            self.check_on(self.red_block, self.shoe_box) and
            self.check_on(self.blue_block, self.shoe_box) and
            self.check_on(self.yellow_block, self.shoe_box)
        )

        # Check if all secondary color blocks are in tray
        secondary_in_tray = (
            self.check_on(self.orange_block, self.tray) and
            self.check_on(self.green_block, self.tray) and
            self.check_on(self.purple_block, self.tray)
        )

        return primary_in_shoe and secondary_in_tray
