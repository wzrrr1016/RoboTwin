from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class container_color_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load the containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Load the blocks
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Load the other objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.mug = self.add_actor("mug", "mug")

    def play_once(self):
        # Pick and place the red block into the fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Pick and place red block:", success)

        # Pick and place the green block into the fluted_block (wrong action)
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Pick and place green block (wrong):", success)

        # Pick the green block from the fluted_block and place it into the dustbin (recovery)
        success = self.pick_and_place(self.green_block, self.dustbin)
        print("Pick and place green block (recovery):", success)

        # Pick and place the yellow block into the fluted_block
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Pick and place yellow block:", success)

        # Pick and place the bottle into the dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Pick and place bottle:", success)

        # Pick and place the cup_without_handle into the dustbin
        success = self.pick_and_place(self.cup_without_handle, self.dustbin)
        print("Pick and place cup_without_handle:", success)

        # Pick and place the mug into the dustbin
        success = self.pick_and_place(self.mug, self.dustbin)
        print("Pick and place mug:", success)

    def check_success(self):
        # Check if all blocks are in the fluted_block and all other objects are in the dustbin
        success = (self.check_on(self.red_block, self.fluted_block) and
                   self.check_on(self.yellow_block, self.fluted_block) and
                   self.check_on(self.green_block, self.dustbin) and
                   self.check_on(self.bottle, self.dustbin) and
                   self.check_on(self.cup_without_handle, self.dustbin) and
                   self.check_on(self.mug, self.dustbin))
        return success
