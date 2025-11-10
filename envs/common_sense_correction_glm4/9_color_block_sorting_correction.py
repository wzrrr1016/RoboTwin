from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load the fluted_block and dustbin
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Load the objects to be sorted
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.toycar = self.add_actor("toycar", "toycar")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.hammer = self.add_actor("hammer", "hammer")
        self.bread = self.add_actor("bread", "bread")

    def play_once(self):
        # Sort the purple block into the fluted_block
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        if not success:
            return self.info

        # Sort the toycar into the dustbin
        success = self.pick_and_place(self.toycar, self.dustbin)
        if not success:
            return self.info

        # Sort the cup_with_handle into the dustbin
        success = self.pick_and_place(self.cup_with_handle, self.dustbin)
        if not success:
            return self.info

        # Sort the hammer into the dustbin
        success = self.pick_and_place(self.hammer, self.dustbin)
        if not success:
            return self.info

        # Sort the bread into the dustbin
        success = self.pick_and_place(self.bread, self.dustbin)
        if not success:
            return self.info

        return True

    def check_success(self):
        # Check if the purple block is on the fluted_block
        if not self.check_on(self.purple_block, self.fluted_block):
            return False

        # Check if the toycar, cup_with_handle, hammer, and bread are on the dustbin
        if not (self.check_on(self.toycar, self.dustbin) and
                self.check_on(self.cup_with_handle, self.dustbin) and
                self.check_on(self.hammer, self.dustbin) and
                self.check_on(self.bread, self.dustbin)):
            return False

        return True

# Note: The Imagine_Task class is assumed to be defined elsewhere in the environment.
