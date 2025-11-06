from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 17_primary_color_organization_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Load objects
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.knife = self.add_actor("knife", "knife")
        self.bottle = self.add_actor("bottle", "bottle")
        self.stapler = self.add_actor("stapler", "stapler")

    def play_once(self):
        # Pick the blue_block from the table and place it into the fluted_block
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("pick place blue_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the blue_block is on the fluted_block
        return self.check_on(self.blue_block, self.fluted_block)
