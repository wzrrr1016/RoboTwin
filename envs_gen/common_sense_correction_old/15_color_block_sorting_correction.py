from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 15_color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.plate = self.add_actor("plate", "plate")
        
        # Add objects
        self.green_block = self.add_actor("green_block", "green_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.toycar = self.add_actor("toycar", "toycar")
        self.mug = self.add_actor("mug", "mug")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")

    def play_once(self):
        # Place blue_block (primary color) into tray
        success = self.pick_and_place(self.blue_block, self.tray)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        # Place green_block (secondary color) into plate
        success = self.pick_and_place(self.green_block, self.plate)
        print("pick place green_block:", success)
        if not success:
            return self.info

        # Place toycar on the table
        success = self.pick_and_place(self.toycar, self.table)
        print("pick place toycar:", success)
        if not success:
            return self.info

        # Place mug into pot-with-plant
        success = self.pick_and_place(self.mug, self.pot_with_plant)
        print("pick place mug:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if blue_block is on tray (primary color)
        if not self.check_on(self.blue_block, self.tray):
            return False

        # Check if green_block is on plate (secondary color)
        if not self.check_on(self.green_block, self.plate):
            return False

        # Check if toycar is on the table
        if not self.check_on(self.toycar, self.table):
            return False

        # Check if mug is on pot-with-plant
        if not self.check_on(self.mug, self.pot_with_plant):
            return False

        return True
