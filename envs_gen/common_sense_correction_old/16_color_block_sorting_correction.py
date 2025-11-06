from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 16_color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load the containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Load the objects to be sorted
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.microphone = self.add_actor("microphone", "microphone")

    def play_once(self):
        # Pick yellow_block and place into coaster
        success = self.pick_and_place(self.yellow_block, self.coaster)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

        # Pick screwdriver and place into dustbin
        success = self.pick_and_place(self.screwdriver, self.dustbin)
        print("pick place screwdriver:", success)
        if not success:
            return self.info

        # Pick microphone and place into dustbin
        success = self.pick_and_place(self.microphone, self.dustbin)
        print("pick place microphone:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if yellow_block is on coaster
        if not self.check_on(self.yellow_block, self.coaster):
            return False

        # Check if screwdriver is on dustbin
        if not self.check_on(self.screwdriver, self.dustbin):
            return False

        # Check if microphone is on dustbin
        if not self.check_on(self.microphone, self.dustbin):
            return False

        return True
