from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class color_block_sorting_correction_44(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.plate = self.add_actor("plate", "plate")
        # Add objects to be sorted
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        # Add the bottle to be placed on the table
        self.bottle = self.add_actor("bottle", "bottle")

    def play_once(self):
        # Pick yellow_block and place it into the tray
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

        # Pick blue_block and place it into the plate
        success = self.pick_and_place(self.blue_block, self.plate)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        # Pick bottle and place it on the table
        success = self.pick_and_place(self.bottle, self.table)
        print("pick place bottle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if yellow_block is on the tray
        yellow_on_tray = self.check_on(self.yellow_block, self.tray)
        # Check if blue_block is on the plate
        blue_on_plate = self.check_on(self.blue_block, self.plate)
        # Check if bottle is on the table
        bottle_on_table = self.check_on(self.bottle, self.table)

        return yellow_on_tray and blue_on_plate and bottle_on_table
