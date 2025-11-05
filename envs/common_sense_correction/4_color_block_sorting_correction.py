from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class color_block_sorting_correction_4(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.tray = self.add_actor("tray", "tray")
        self.plate = self.add_actor("plate", "plate")
        # Load objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.mug = self.add_actor("mug", "mug")

    def play_once(self):
        # Place red_block into tray
        success = self.pick_and_place(self.red_block, self.tray)
        print("pick place red_block:", success)
        if not success:
            return self.info

        # Place blue_block into tray
        success = self.pick_and_place(self.blue_block, self.tray)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        # Place green_block into plate
        success = self.pick_and_place(self.green_block, self.plate)
        print("pick place green_block:", success)
        if not success:
            return self.info

        # Place yellow_block into tray
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

        # Place mug on table
        success = self.pick_and_place(self.mug, self.table)
        print("pick place mug:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all primary color blocks are on the tray
        if (self.check_on(self.red_block, self.tray) and
            self.check_on(self.blue_block, self.tray) and
            self.check_on(self.yellow_block, self.tray)):

            # Check if the secondary color block is on the plate
            if self.check_on(self.green_block, self.plate):

                # Check if the mug is on the table
                if self.check_on(self.mug, self.table):
                    return True

        return False
